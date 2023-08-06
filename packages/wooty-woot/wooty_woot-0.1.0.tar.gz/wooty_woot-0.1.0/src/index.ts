import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ILauncher } from '@jupyterlab/launcher';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { imageIcon } from '@jupyterlab/ui-components';
import { requestAPI } from './handler';

/**
 * Initialization data for the wooty_woot extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'wooty_woot:plugin',
  autoStart: true,
  optional: [ISettingRegistry, ILauncher, IFileBrowserFactory],
  activate: (
    app: JupyterFrontEnd, 
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher | null,
    fileBrowser: IFileBrowserFactory,
  ) => {
    console.log('JupyterLab extension wooty_woot is activated!');

    // Load the settings from schema/plugin.json
    // This can include adding commands to a context menu
    // or to the main or other menu
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('wooty_woot settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for wooty_woot.', reason);
        });
    }

    app.commands.addCommand('wooty_woot:open', {
      // code to run when this command is executed
      execute: () => {
        // const widget = new TutorialWidget();
        // const main = new MainAreaWidget({ content: widget });
        // const button = new ToolbarButton({icon: refreshIcon, onClick: () => widget.load_image()});

        // main.title.label = 'Tutorial Widget';
        // main.title.icon = imageIcon;
        // main.title.caption = widget.title.label;

        // // TODO: add a button to refresh image
        // main.toolbar.addItem('Refresh', button);
        // app.shell.add(main, 'main');
        const reply = requestAPI<any>(
          'viewer', 
          {
            body: JSON.stringify({'path': fileBrowser.defaultBrowser.model.path}), 
            method: 'POST'
          }
        );
        console.log("Aaaand I'm back", reply);
        // widget.make_a_file(fileBrowser.defaultBrowser.model.path);
      },
      icon: imageIcon,
      label: 'Open Tutorial Widget'
    });

    // Add item to launcher
    if (launcher) {
      launcher.add({
        command: 'wooty_woot:open',
        category: 'Moo'
      });
    }

    requestAPI<any>('viewer')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The wooty_woot server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
