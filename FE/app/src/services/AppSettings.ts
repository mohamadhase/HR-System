import { HttpClient,HttpHeaders } from "@angular/common/http";
export class AppSettings{
    public static get API_ENDPOINT():string{
        return 'http://localhost:5000/';
    }
    public static get HEADER():HttpHeaders{
        return  new HttpHeaders({
            'Content-Type': 'application/json',
            'x-acess-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJVc2VyTmFtZSI6InN0cmluZyIsImV4cCI6MTY1OTcxNDQ0N30.15aMChRe3HypNJ4a_OwiE4ieI33WZpJzoERjWOi_YeI'
          })
    }
}