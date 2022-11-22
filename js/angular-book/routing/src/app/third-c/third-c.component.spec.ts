import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThirdCComponent } from './third-c.component';

describe('ThirdCComponent', () => {
  let component: ThirdCComponent;
  let fixture: ComponentFixture<ThirdCComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ThirdCComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ThirdCComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
