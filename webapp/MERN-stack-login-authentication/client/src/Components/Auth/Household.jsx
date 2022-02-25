import React from "react";
import './styles.css'

var mqtt = require('mqtt')
  
var mqtt = require('mqtt')
var client = mqtt.connect('mqtt://test.mosquitto.org:8080', {clientId:"clientId-nNHnQSchDy"})
console.log("connected flag  " + client.connected);

client.on("connect",function(){	
console.log("connected  "+ client.connected);
})

//handle errors
client.on("error",function(error){
console.log("Can't connect" + error);
process.exit(1)});

//publish
function publish(message){
console.log("publishing topic: instruction", " message: ", message);

if (client.connected == true){
    client.publish('household', message);
}
}

class Household extends React.Component {
  constructor(props) {
    super(props)
    this.state = { 
       formValues: [{ name: "", number : "" }]
     };
    this.handleSubmit = this.handleSubmit.bind(this)
  } 
  
  handleChange(i, e) {
    let formValues = this.state.formValues;
    formValues[i][e.target.name] = e.target.value;
    this.setState({ formValues });
  }

  addFormFields() {
    this.setState(({
      formValues: [...this.state.formValues, { name: "", number: "" }]
    }))
  }

  removeFormFields(i) {
    let formValues = this.state.formValues;
    formValues.splice(i, 1);
    this.setState({ formValues });
  }

  handleSubmit(event) {
    event.preventDefault();
    alert(JSON.stringify(this.state.formValues));
    publish(JSON.stringify(this.state.formValues));
  }

  render() {

    return (
        <div> 
            <h1 className="text-capitalize">
             hello </h1>
        
        <form  onSubmit={this.handleSubmit}>
          {this.state.formValues.map((element, index) => (
            <div className="form-inline" key={index}>
              <label>Name</label>
              <input type="text" name="name" value={element.name || ""} onChange={e => this.handleChange(index, e)} />
              <label>Number</label>
              <input type="text" name="number" value={element.number || ""} onChange={e => this.handleChange(index, e)} />
              {
                index ? 
                  <button type="button"  className="button btn-danger remove" onClick={() => this.removeFormFields(index)}>Remove</button> 
                : null
              }
            </div>
          ))}
          <div className="button-section">
              <button className="button btn-md add" type="button" onClick={() => this.addFormFields()}>Add</button>
              <button className="button submit" type="submit">Submit</button>
          </div>
      </form>
      </div>
    );
  }
}
export default Household;