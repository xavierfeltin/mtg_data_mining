import { TestBed, inject } from '@angular/core/testing';

import { CardServiceService } from './card-service.service';

describe('CardServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CardServiceService]
    });
  });

  it('should be created', inject([CardServiceService], (service: CardServiceService) => {
    expect(service).toBeTruthy();
  }));
});
