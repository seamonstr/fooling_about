import { formatCurrency } from '@angular/common';
import {Component} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { firstValueFrom } from 'rxjs';

@Component ({
    selector: 'login',
    templateUrl: './login.component.html',
})
export class LoginComponent {

    loginForm = this.fb.group({
        userName: ['', [Validators.required, Validators.minLength(6)]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        dog: this.fb.group({
            collarSize: ['', Validators.required],
            dogName: ['', Validators.required],
        })
    });

    focussed: undefined | FormControl = undefined;

    constructor(private fb: FormBuilder) {
        this.loginForm.controls.userName.valueChanges.subscribe(
            (e) => console.log(`Updated to ${e?.toString()}`));
        console.log(this.loginForm);
    }

    findControlByName(name: string, from: FormGroup): FormControl | undefined {
        for (let i in from.controls) {
            if (i == name && from.controls[i] instanceof FormControl)
                return from.controls[i] as FormControl;
            if (from.controls[i] instanceof FormGroup)
                return this.findControlByName(name, from.controls[i] as FormGroup);
        }
        return undefined;
    }

    onFocus(event: Event) {
        let controlName = (event.target as HTMLInputElement).name;
        this.focussed = this.findControlByName(controlName, this.loginForm);
    }

    onBlur(event: Event) {
        this.focussed = undefined;
    }

    onSubmit() {
        console.log("Saved stuff");
    }

    updateName(name: string) {
        this.loginForm.controls.userName.setValue(name);
    }

    getControlClass(control: FormControl): string {
        if (control.pristine || control == this.focussed)
            return '';

        return control.dirty && control.invalid ? 'is-invalid' : 'is-valid';
    }
}