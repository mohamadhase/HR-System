import { Component, OnInit } from '@angular/core';
import { Team } from 'src/models/Team';
import { TeamService } from 'src/services/team.service';
import { catchError } from 'rxjs/operators';
@Component({
  selector: 'app-teams',
  templateUrl: './teams.component.html',
  styleUrls: ['./teams.component.css']
})
export class TeamsComponent implements OnInit {
  Teams: Array<Team> = [];
  constructor(private teamService: TeamService) { }

  ngOnInit(): void {
    this.Teams = this.teamService.getTeams();
  }
  deleteTeam(team: Team): void {
    if (confirm(`Are you sure to delete ${team.Name}?`)) {
      this.teamService.deleteTeam(team.Name);
    this.Teams.splice(this.Teams.indexOf(team), 1);
    alert(`Team ${team.Name} deleted`);
    }

    
  }
  updateTeam(team: Team): void {
    let input = document.getElementById('teamDescription') as HTMLInputElement;
    // check if the input is empty
    if (input?.value == '') {
      alert('Please enter a description');
    }
    else {
      this.teamService.updateTeam(team, input.value);
      team.Description = input.value;
      alert(`Team ${team.Name} updated`);
    }

  }
  newTeam() {
    let nameInput = document.getElementById('teamName') as HTMLInputElement;
    let descriptionInput = document.getElementById('teamDescription') as HTMLInputElement;
    let Error = document.getElementById('Error') as HTMLParagraphElement;
    let code = 200;
    let team: Team = {} as Team;
    // check if the input is empty
    if (nameInput?.value == '' || descriptionInput?.value == '') {
      alert('Please enter a name and description');
    }
    else {
      team = {
        Name: nameInput.value,
        Description: descriptionInput.value
      }
      this.teamService.newTeam(team).pipe(
        catchError(error => {
          Error.innerHTML = `the team ${team.Name} already exists`;
          return ([]);
        })
      ).subscribe(
        data => {
          this.Teams.push(team);
          Error.innerHTML = `Team ${team.Name} created`;
          Error.style.color = 'green';
        }
      )


    }


  }

}
