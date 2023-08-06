import {
    JupyterFrontEnd,
    ILayoutRestorer,
    JupyterFrontEndPlugin
  } from '@jupyterlab/application';

import { DocumentRegistry } from '@jupyterlab/docregistry';
import {
    NotebookPanel,
    INotebookModel,
    // NotebookActions,
  } from '@jupyterlab/notebook';
import { DisposableDelegate, IDisposable } from '@lumino/disposable';
import {
    ICommandPalette,
  } from '@jupyterlab/apputils';
import { ICurrentUser } from '@jupyterlab/user';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';

import { ToolbarButton } from '@jupyterlab/apputils';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { SolutionViewModel, SolutionViewWidget } from './solutionWidget';


class ButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>{
    createNew(widget: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): void | IDisposable {

        function callback(){
            const keySolutionWidgetMap = new Map<string, SolutionViewWidget>();

            widget.content.widgets.forEach((cell, index) => {

                var solutionViewModel = new SolutionViewModel();
                var solutionViewWidget = new SolutionViewWidget(solutionViewModel);

                keySolutionWidgetMap.set(cell.model.metadata.get('cellID') as string, solutionViewWidget);

                (cell.layout as any).addWidget(solutionViewWidget);
            })


            const ydoc = new Y.Doc();

            const websocketProvider = new WebsocketProvider(
                'ws://localhost:1234', 'count-demo', ydoc
            );
            websocketProvider.connect();

            const keyCellMap = new Map<string, number>();

            widget.content.widgets.forEach((cell, index) => {
                keyCellMap.set(cell.model.metadata.get('cellID') as string, index);
            })

            // bind observer
            function bindObserver(){
                for (const studentName of ydoc.share.keys()){
                    const studentSource = ydoc.getMap(studentName);

                    studentSource.observe(event => {
                        event.changes.keys.forEach((change, key) => {
                            if (change.action==='delete'){return;}
                            if (key.endsWith('-output')){
                                const kkey = key.slice(0, -7);
                                if (keyCellMap.has(kkey)){
                                    (keySolutionWidgetMap.get(kkey) as SolutionViewWidget).model.setOutput(studentName, ((event.currentTarget as Y.Map<any>).get(key) as Y.Array<any>).toArray());
                                }
                            }else{
                                if (keyCellMap.has(key)){
                                    const masterCopy = widget.content.widgets[keyCellMap.get(key) as number].model.sharedModel.getSource();
                                    var solutionViewWidget = keySolutionWidgetMap.get(key) as SolutionViewWidget;
                                    solutionViewWidget.model.setSolution(studentName, ((event.currentTarget as Y.Map<any>).get(key) as Y.Text).toString(), masterCopy);
                                }
                            }
                        })
                    })
                }
            }

            // ydoc shared keys are not loaded yet
            websocketProvider.on('sync', ()=> {
                bindObserver();
            })

        }
        const button = new ToolbarButton({
            className: 'sharing-button',
            label: 'Real Time View',
            onClick: callback,
            tooltip: 'Start Sharing'
        });

        widget.toolbar.insertItem(11, 'realtimebutton', button);
        return new DisposableDelegate(() => {
            button.dispose();
          });
    }
}

const pluginShare: JupyterFrontEndPlugin<void> = {
    id: 'ovservacode:share-plugin',
    autoStart: true,
    requires: [ICurrentUser, ICommandPalette, IRenderMimeRegistry, ILayoutRestorer],
    activate: activatePluginTest
}
  


function activatePluginTest(
    app: JupyterFrontEnd,
    user: ICurrentUser,
    palette: ICommandPalette,
    rendermime: IRenderMimeRegistry,
    restorer: ILayoutRestorer    
): void {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());

}
  
export default pluginShare;