import {
  Component,
  DoCheck,
  OnChanges,
  OnInit,
  SimpleChanges,
} from '@angular/core';
import { CounterExercisesService } from './counter-exercises.service';

@Component({
  selector: 'app-counter-exercises',
  templateUrl: './counter-exercises.component.html',
  styleUrls: ['./counter-exercises.component.scss'],
})
export class CounterExercisesComponent implements OnInit, DoCheck {
  exercises!: any;

  constructor(private counterExercises: CounterExercisesService) {}

  ngOnInit(): void {
    this.counterExercises.getCounterExercises().subscribe((data) => {
      this.exercises = data;
    });
  }

  ngDoCheck(): void {
    /*this.counterExercises.getCounterExercises().subscribe((data) => {
      this.exercises = data;
    });*/
  }
}
