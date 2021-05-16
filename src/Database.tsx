import React, { useReducer, useState, useEffect } from "react";
import Send from '@material-ui/icons/Send';
import { Button, TextField, Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { DataGrid, GridRowsProp, GridColDef } from "@material-ui/data-grid";
import apiRequest, { ApiRequest } from './Api';
import { getConfig } from './Config';

const rows: GridRowsProp = [
];

const columns: GridColDef[] = [
  { field: "id", hide: true },
  { field: "first_name", headerName: "First Name", width: 150 },
  { field: "last_name", headerName: "Last Name", width: 150 }
];

function Database(props: { formName: string, formDescription: string }) {
  const useStyles = makeStyles(theme => ({
    button: {
      margin: theme.spacing(1)
    },
    leftIcon: {
      marginRight: theme.spacing(1)
    },
    iconSmall: {
      fontSize: 20
    },
    root: {
      padding: theme.spacing(3, 2)
    },
    container: {
      display: "flex",
      flexWrap: "wrap"
    },
    textField: {
      marginLeft: theme.spacing(1),
      marginRight: theme.spacing(1),
      width: 400
    }
  }));
  const [users, setUsers] = useState(rows);
  const [formInput, setFormInput] = useReducer(
    (state: any, newState: any) => ({ ...state, ...newState }),
    {
      firstName: '',
      lastName: '',
    }
  );
  const getUsers = () => {
    const request: ApiRequest = {
      url: getConfig().exampleServer + '/api/crossplane/users',
      method: 'GET',
    };
    apiRequest(request).then(users => {
      setUsers(users.users)
    });
  };
  useEffect(() => {
    getUsers();
  }, []);
  const submit = (evt: any) => {
    evt.preventDefault();
    const request: ApiRequest = {
      url: getConfig().exampleServer + '/api/crossplane',
      method: 'POST',
      body: formInput,
    };
    apiRequest(request).then(response => {
      getUsers();
    });
  };
  const handleInput = (evt: any) => {
    const name = evt.target.name;
    const newValue = evt.target.value;
    setFormInput({ [name]: newValue });
  };
  const classes = useStyles();
  return (
    <div>
      <Paper className={classes.root}>
        <Typography variant="h5" component="h3">
          {props.formName}
        </Typography>
        <Typography component="p">{props.formDescription}</Typography>
        <form onSubmit={submit}>
          <TextField
            label="First Name"
            id="margin-normal"
            name="firstName"
            defaultValue={formInput.firstName}
            className={classes.textField}
            helperText="Enter your first name e.g. John"
            onChange={handleInput}
          />
          <TextField
            label="Last Name"
            id="margin-normal"
            name="lastName"
            defaultValue={formInput.lastName}
            className={classes.textField}
            helperText="Enter your last name e.g. Doe"
            onChange={handleInput}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            className={classes.button}
            endIcon={<Send/>}
          >
            Create
          </Button>
        </form>
      </Paper>
      <DataGrid rows={users} columns={columns} />
    </div>
  );
}

export default Database;
