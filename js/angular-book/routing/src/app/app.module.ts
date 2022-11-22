import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { Router, RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { FirstComponent } from './first/first.component';
import { SecondComponent } from './second/second.component';
import { ThirdComponent } from './third/third.component';
import { ThirdAComponent } from './third-a/third-a.component';
import { ThirdBComponent } from './third-b/third-b.component';
import { ThirdCComponent } from './third-c/third-c.component';
import { ThirdBAComponent } from './third-ba/third-ba.component';
import { QuothTheServerComponent } from './quoth-the-server/quoth-the-server.component';

const routes: Routes = [
  {path: 'first', component: FirstComponent},
  {path: 'second', component: SecondComponent},
  {path: 'third/stuff/:myparm', component: ThirdComponent, children: [
    {path: 'thirdA', component: ThirdAComponent},
    {path: 'thirdB/another', component: ThirdBComponent, children: [
      {path: 'thirdBA', component: ThirdBAComponent},
    ]},
    {path: 'thirdC', component: ThirdCComponent},
  ]},
  {path: '**', component: QuothTheServerComponent}      

];

@NgModule({
  declarations: [
    AppComponent,
    FirstComponent,
    SecondComponent,
    ThirdComponent,
    ThirdAComponent,
    ThirdBComponent,
    ThirdCComponent,
    ThirdBAComponent,
    QuothTheServerComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes, )
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { 
  constructor(private router: Router) {}
}
