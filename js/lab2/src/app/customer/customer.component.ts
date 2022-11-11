import { NgFor } from '@angular/common';
import { NONE_TYPE } from '@angular/compiler';
import { Component, Output, Input, EventEmitter, ViewChild } from '@angular/core';
import { NgForm, NgModel } from '@angular/forms';
import { Customer } from '../models/customer';

@Component({
  selector: 'customer',
  templateUrl: './customer.component.html',
})
export class CustomerComponent {
  firstName: string = "";
  lastName: string = "";
  customers: Array<Customer>;
  isAddNew: boolean = false;

  constructor() {
    this.customers = new Array<Customer>();
    this.customers.push(new Customer('Bob', 'Bobberson'));
    this.customers.push(new Customer('Chubby', 'Chops'));
    this.customers.push(new Customer('Yippie', 'Kaiyay'));
    this.customers.push(new Customer('Whoo', 'Hoo'));
  }

  @ViewChild('myForm')
  customerForm: NgForm | undefined = undefined;

  getValue(event: Event): string {
    console.log(event)
    return (event.target as HTMLInputElement).value;
  }

  save(FName?: string, LName?: string) {
    if (this.firstName == undefined || this.lastName == undefined)
      return
    this.customers.push(new Customer(this.firstName, this.lastName))
    this.isAddNew = false;
    this.reset();
  }

  reset() {
    this.customerForm?.reset();
  }

  addNew() {
    this.isAddNew = true;
  }

  cancelAddNew() {
    this.isAddNew = false;
  }
}
