import { HttpClient,HttpHeaders } from "@angular/common/http";
export class AppSettings{
    public static get API_ENDPOINT():string{
        return 'https://training2-project.ew.r.appspot.com/';
    }
    public static get HEADER():HttpHeaders{
        return  new HttpHeaders({
            'Content-Type': 'application/json',
            'x-acess-token': String(localStorage.getItem('token'))
          })

    }

    public static get SLACK_TOKEN():string{
        return 'xoxb-3867696838934-3874233291827-guuIX06ME5hZHeYbAkMzcbVU';
    }
    public static get SLACK_END_POINT():string{
        return 'https://slack.com/api/';
    }
    public static get SLACK_HEADER():HttpHeaders{
        
        return  new HttpHeaders({
           'Content-type':'application/x-www-form-urlencoded'

          })
    }
}