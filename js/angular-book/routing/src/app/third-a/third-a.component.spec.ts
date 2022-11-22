import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThirdAComponent } from './third-a.component';

describe('ThirdAComponent', () => {
  let component: ThirdAComponent;
  let fixture: ComponentFixture<ThirdAComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ThirdAComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ThirdAComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
