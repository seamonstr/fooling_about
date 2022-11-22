import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThirdBAComponent } from './third-ba.component';

describe('ThirdBAComponent', () => {
  let component: ThirdBAComponent;
  let fixture: ComponentFixture<ThirdBAComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ThirdBAComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ThirdBAComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
