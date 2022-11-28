import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CounterExercisesService {

  constructor(private http: HttpClient) { }

  getCounterExercises(): Observable<any> {
    return this.http.get('http://192.168.1.1:8000/inferences/countbytype');
  }
}
