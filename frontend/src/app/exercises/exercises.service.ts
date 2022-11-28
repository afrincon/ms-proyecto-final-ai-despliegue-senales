import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ExercisesService {

  constructor(private http: HttpClient) { }

  getListExercises() {
    return this.http.get('http://192.168.1.1:8080/inferences');
  }
}
