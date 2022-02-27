import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { registerUser, logoutUser } from '../../redux/actions/authActions';
import './Navbar.css';

class Navbar extends Component {
  render() {
    const isAuthenticated = this.props.auth.isAuthenticated
    return (
      <nav className="navbar navbar-expand-md navbar-dark fixed-top">
        <div className="container">
          <Link className="navbar-brand border-none" to={isAuthenticated ? "/dashboard" : "/"}>
            Toilet.io
          </Link>
          <button
            className="navbar-toggler d-lg-none"
            type="button"
            data-toggle="collapse"
            data-target="#collapsibleNavId"
            aria-controls="collapsibleNavId"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="collapsibleNavId">
            <ul className="navbar-nav ml-auto mt-2 mt-lg-0">
              {
                isAuthenticated
                  ? <>
                    <li className="nav-item">
                      <Link
                        className="nav-link btn btn-register button-outline-none"
                        onClick={() => {
                          this.props.logoutUser()
                        }}
                      >
                        Logout
                      </Link>
                    </li>
                  </>
                  : <>
                    <li className="nav-item">
                      <Link
                        className="nav-link btn btn-login button-outline-none"
                        to="/login"
                      >
                        Login
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link
                        className="nav-link btn btn-register button-outline-none"
                        to="/register"
                      >
                        Signup
                      </Link>
                    </li>
                  </>
              }
            </ul>
          </div>
        </div>
      </nav>
    );
  }
}

Navbar.propTypes = {
  registerUser: PropTypes.func.isRequired,
  logoutUser: PropTypes.func.isRequired,
  auth: PropTypes.object.isRequired,
  errors: PropTypes.object.isRequired
};

const mapStateToProps = state => ({
  auth: state.auth,
  errors: state.errors
});

export default connect(mapStateToProps, { registerUser, logoutUser })(withRouter(Navbar));
