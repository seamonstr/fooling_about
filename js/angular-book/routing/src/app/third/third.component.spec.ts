import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThirdComponent } from './third.component';

describe('ThirdComponent', () => {
  let component: ThirdComponent;
  let fixture: ComponentFixture<ThirdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ThirdComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ThirdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
