import React, { Component, useReducer } from 'react';
import {Collapse,Navbar,NavbarToggler,NavbarBrand,Nav,NavItem,NavLink,UncontrolledDropdown,
 Button, Input, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, Table, Form, FormGroup, Container, Label, InputGroup} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import {Helmet} from 'react-helmet'

  class PageNotFound extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
      super(props);
      this.state = {

    };
    }	

    componentDidMount() {

  }

    render() {
      return (
        <div style={{minHeight: '650px'}}>
          <Helmet>
          <title>Page not found | E-Health</title>
          </Helmet>
          <Container>
              <br/>
              <h1 style={{marginTop: '120px', fontWeight: 'bold'}}>
                404 - Page Not Found
              </h1>
              <h5 style={{marginTop: '80px'}}>
                The page you're looking for has not been found, please check your link and try again
              </h5>
              <br/><br/>
              <a href='/' style={{color: 'inherit'}}>
                  Click here to visit our homepage instead
              </a>
          </Container>
        </div>
      );
    }

  };
  
  export default withCookies(PageNotFound);