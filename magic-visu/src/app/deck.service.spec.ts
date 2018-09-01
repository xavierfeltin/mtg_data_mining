import { TestBed, inject } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DeckService } from './deck.service';

describe('DeckService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DeckService]
    });
  });

  it('should be created', inject([DeckService], (service: DeckService) => {
    expect(service).toBeTruthy();
  }));
});
