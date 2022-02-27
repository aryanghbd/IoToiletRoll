import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { logoutUser } from '../../redux/actions/authActions';
import './Dashboard.css';
import { Link } from 'react-router-dom';

class Dashboard extends Component {
  onLogoutClick = e => {
    e.preventDefault();
    this.props.logoutUser();
  };



  render() {
    const { user } = this.props.auth;
    return (
      <section className="dashboard">
        <div className="container">
          <div className="row">
            <div className="col-12">
              <div className="content">
                <h1>
                  Hi <b>{user.name.split(' ')[0]} </b>
                </h1>
                {/* <Link className="btn btn-lg btn-warning mt-5" to={"/household"}>
                  Edit Household
                </Link> */}
                <Link className="btn btn-lg btn-warning mt-5" to={"/leaderboard"}>
                  Leaderboard
                </Link>
                <Link className="btn btn-lg btn-warning mt-5" onClick={this.onLogoutClick}>
                  Logout
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

Dashboard.propTypes = {
  logoutUser: PropTypes.func.isRequired,
  auth: PropTypes.object.isRequired
};

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(mapStateToProps, { logoutUser })(Dashboard);

