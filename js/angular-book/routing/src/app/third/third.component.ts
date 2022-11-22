import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-third',
  templateUrl: './third.component.html',
  styleUrls: ['./third.component.css']
})
export class ThirdComponent implements OnInit {

  parm!: string | null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.parm = this.route.snapshot.paramMap.get('myparm');
  }
}
