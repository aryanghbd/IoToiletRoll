import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { DropDown } from 'dynamic-dropdown'
import 'dynamic-dropdown/dist/index.css'
import { connect } from 'react-redux';
import './Rolling.css';

var mqtt = require('mqtt')

var client = mqtt.connect('mqtt://test.mosquitto.org:8080')

// handle connect
client.on("connect", function () {
  console.log("connected  " + client.connected);
})

// handle messages
client.on("message", function(topic, payload) {
})

// handle errors - exit
client.on("error", function (error) {
  console.log("Can't connect" + error);
  process.exit(1)
});

function publishUser (user) {
    console.log("publishing topic: user", " message: ", user);
    console.log(user)
    if (client.connected == true) {
      client.publish('user', user)
    }
}

class Rolling extends Component{
    constructor(props) { 
        super(props)
        this.state = {
          users: props.rolling,
          formValue: ""
        };
        this.handleSubmit = this.handleSubmit.bind(this)
        this.onChangeForm = this.onChangeForm.bind(this);
      }

      onChangeForm(e) {
          console.log(e.target.value)
        this.setState({
            formValue: e.target.value
        });
      }

    //  <DropDown onChange = {this.onChangeForm}
    //  elements={this.state.users}
    //  selection={{ width: 300, borderRadius: 10 }}
    ///>


      handleSubmit(event) {
        event.preventDefault();
        publishUser(this.state.formValue)
        this.props.history.push("/dashboard")
      }

render(){
   {
       let options = this.state.users.map((x)=>{
           return(
               <option key={x.name}>
                   {x.name}
               </option>
           )
       })
   
  return (
    <form onSubmit={this.handleSubmit}>
    <div className="container" style={{ marginTop: 100 }}>

    <select name="users" id="users" onChange={this.onChangeForm} >
    {options}
    </select>
    <div>
    <button style={{marginRight: 100}} type="submit" className="btn btn-md btn-register">
    Submit
    </button>
    </div>
    </div>
    </form>
  )
}
}
}


Rolling.propTypes = {
    rolling: PropTypes.array.isRequired
  };

  
  const mapStateToProps = state => ({
    rolling: state.rolling.rolling
  });
  
  export default connect(mapStateToProps, {})(Rolling);
