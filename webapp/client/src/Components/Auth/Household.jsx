import React from "react";
import './styles.css';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { publishHousehold } from "../../redux/actions/mqttActions"

class Household extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      formValues: [{ name: "", number: "" }]
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
    var json = JSON.stringify(this.state.formValues);
    this.props.publishHousehold(json)
    this.props.history.push("/dashboard")
  }

  render() {

    return (
      <div className="container" style={{ marginTop: 56 }}>
        <h1 style={{textAlign: "center", padding: "16px 0"}}>Household Members</h1>
        <form onSubmit={this.handleSubmit}>
          {this.state.formValues.map((element, index) => (
            <div className="form-inline" key={index}>
              <label>Name</label>
              <input type="text" name="name" value={element.name || ""} onChange={e => this.handleChange(index, e)} />
              <label>Phone Number</label>
              <input type="tel" name="number" value={element.number || ""} onChange={e => this.handleChange(index, e)} />
              <button type="button" style={{
                visibility: index == 0 ? "hidden" : "visible"
              }} className="button btn-danger remove" onClick={() => this.removeFormFields(index)}>Remove</button>
            </div>
          ))}
          <div className="button-section">
            <button style={{marginRight: 8}} className="button btn-md add" type="button" onClick={() => this.addFormFields()}>Add</button>
            <button className="button submit" type="submit">Submit</button>
          </div>
        </form>
      </div>
    );
  }
}

Household.propTypes = {
  publishHousehold: PropTypes.func.isRequired,
};

const mapStateToProps = state => ({});

export default connect(mapStateToProps, { publishHousehold })(Household);