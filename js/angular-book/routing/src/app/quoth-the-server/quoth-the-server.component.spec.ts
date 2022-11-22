import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuothTheServerComponent } from './quoth-the-server.component';

describe('QuothTheServerComponent', () => {
  let component: QuothTheServerComponent;
  let fixture: ComponentFixture<QuothTheServerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ QuothTheServerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuothTheServerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
