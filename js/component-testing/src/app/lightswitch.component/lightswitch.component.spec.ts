import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { LightSwitchComponent } from './lightswitch.component';

describe("LightswitchComponent class tests", () => {
    let comp: LightSwitchComponent;

    beforeEach(function () {
        comp = new LightSwitchComponent();
    });

    it("ensures initial state starts as 'off'", function () {
        expect(comp?.lightOn).toBe(false);
    });

    it("checks that component-click inverts the internal state", function () {
        comp.flipLightSwitch();
        expect(comp.lightOn).toBe(true);
        comp.flipLightSwitch();
        expect(comp.lightOn).toBe(false);
    });

    it("Does some arbitrary thing that nobody cares about", function () {
        expect(true).toBe(true);
    });
})

describe('LightSwitchComponent component tests', () => {
    let fixture: ComponentFixture<LightSwitchComponent>;
    let compInstance: LightSwitchComponent;
    let compDomElement: any;


    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [
                RouterTestingModule
            ],
            declarations: [
                LightSwitchComponent
            ],
        }).compileComponents();
        fixture = TestBed.createComponent(LightSwitchComponent);
        compInstance = fixture.componentInstance;
        compDomElement = fixture.debugElement.nativeElement;

    });

    it('should create the app', () => {
        expect(compInstance).toBeTruthy();
    });

    it(`Should flip lightswitch state on click`, () => {
        // const compDomElement = fixture.debugElement.nativeElement;
        compDomElement.querySelector('.lightswitch-button')?.click();
        expect(compInstance.lightOn).toBe(true);
        compDomElement.querySelector('.lightswitch-button')?.click();
        expect(compInstance.lightOn).toBe(false);
    });

    it(`Should set text correctly on click`, () => {
        fixture.detectChanges(); 
        console.log(compDomElement.querySelector('.lightswitch-text'));
        expect(compDomElement.querySelector('.lightswitch-text')?.textContent).toContain("off");
        compInstance.flipLightSwitch();
        fixture.detectChanges(); 
        expect(compDomElement.querySelector('.lightswitch-text')?.textContent).toContain("on");
        compInstance.flipLightSwitch();
        fixture.detectChanges(); //
        expect(compDomElement.querySelector('.lightswitch-text')?.textContent).toContain("off");
    });
});
