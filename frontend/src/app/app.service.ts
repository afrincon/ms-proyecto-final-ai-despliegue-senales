import { Injectable } from '@angular/core';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { Observable } from 'rxjs';

@Injectable()
export class AppService {

  private endpoint: string;

  constructor(private _mqttService: MqttService) {
    this.endpoint = '/fastapi/mqtt/';
   }

   topic(topic: string): Observable<IMqttMessage> {
     let topicName = this.endpoint + topic;
     console.log('topicName: ' + topicName);
     return this._mqttService.observe(topicName);
   }
}
