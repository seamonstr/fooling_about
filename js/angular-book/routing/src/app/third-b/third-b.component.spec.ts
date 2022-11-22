import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThirdBComponent } from './third-b.component';

describe('ThirdBComponent', () => {
  let component: ThirdBComponent;
  let fixture: ComponentFixture<ThirdBComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ThirdBComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ThirdBComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
