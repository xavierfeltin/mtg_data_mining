import { TestBed, inject } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ModelService } from './model.service';

describe('ModelService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ModelService]
    });
  });

  it('should be created', inject([ModelService], (service: ModelService) => {
    expect(service).toBeTruthy();
  }));
});
