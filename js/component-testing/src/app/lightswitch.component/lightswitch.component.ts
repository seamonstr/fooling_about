import { Component } from "@angular/core";

@Component({
    selector: 'lightswitch',
    templateUrl: './lightswitch.component.html',
    styleUrls: ['./lightswitch.component.css'],
})
export class LightSwitchComponent {
    lightOn: boolean = false;

    flipLightSwitch() {
        this.lightOn = !this.lightOn;
    }

}