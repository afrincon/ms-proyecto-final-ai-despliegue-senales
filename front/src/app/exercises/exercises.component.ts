import { Component, OnInit } from '@angular/core';
import { ExercisesService } from './exercises.service';

@Component({
  selector: 'app-exercises',
  templateUrl: './exercises.component.html',
  styleUrls: ['./exercises.component.scss']
})
export class ExercisesComponent implements OnInit {

  exercisesList!: any;

  constructor(private exercises: ExercisesService) { }

  ngOnInit(): void {
    this.exercises.getListExercises().subscribe((data) => {
      this.exercisesList = data;
      console.log(data)
    });
  }

}
