import { Component, OnDestroy } from '@angular/core';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnDestroy {
  title = 'front-ms';
  private subscription: Subscription;
  public message!: string;
  public inference!: string;
  public exercise!: string;

  constructor(private _mqttService: MqttService) {
    console.log('AppComponent constructor');
    this.subscription = this._mqttService.observe('/fastapi/mqtt/inference').subscribe((message: IMqttMessage) => {
      this.message = message.payload.toString();
      this.processMessage();
    });
  }

  public unsafePublish(topic: string, message: string): void {
    this._mqttService.unsafePublish(topic, message, {qos: 1, retain: true});
  }

  public ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  public processMessage() {
    let inferences = this.message;

    let dictionaryViaLiteral: any = {};

    inferences.split(',').forEach((item) => {
      let inference_intern = item.split(':');
      dictionaryViaLiteral[inference_intern[0]] = parseFloat(inference_intern[1]);
    });

    for (let item in dictionaryViaLiteral) {
      dictionaryViaLiteral[item] = dictionaryViaLiteral[item] * 100;
      if (dictionaryViaLiteral[item] > 85) {
        this.exercise = item;
        this.inference = dictionaryViaLiteral[item].toString();
      }

    }

  }

}
