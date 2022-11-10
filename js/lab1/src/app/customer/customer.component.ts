import { Component } from '@angular/core';
import { Customer } from '../models/customer';

@Component({
  selector: 'customer',
  templateUrl: './customer.component.html',
})
export class CustomerComponent {
  firstName: string;
  lastName: string;
  customers: Array<Customer>;
  isAddNew: boolean;

  constructor() {
    this.isAddNew = false;
    this.firstName = "FirstName";
    this.lastName = "Surname";

    this.customers = new Array<Customer>();
    this.customers.push(new Customer('Bob', 'Bobberson'));
    this.customers.push(new Customer('Chubby', 'Chops'));
    this.customers.push(new Customer('Yippie', 'Kaiyay'));
    this.customers.push(new Customer('Whoo', 'Hoo'));
  }

gronk() {
    return "gronk!"
}
  setFirstName(value:string) {
    this.firstName = value;
  }

  setLastName(value: string) {
    this.lastName = value;
  }

  save(FName?: string, LName?: string ) {
    if (this.firstName == undefined || this.lastName == undefined)
        return
    this.customers.push(new Customer(this.firstName, this.lastName))
    this.isAddNew = false;
    console.log(`Saved ${FName} ${LName}`)
  }

  addNew() {
    this.isAddNew = true;
  }

  cancelAddNew() {
    this.isAddNew = false;
  }
}
