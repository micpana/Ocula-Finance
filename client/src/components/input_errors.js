import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import { Helmet } from 'react-helmet'
import {
    Audio,
    BallTriangle,
    Bars,
    Circles,
    Grid,
    Hearts,
    Oval,
    Puff,
    Rings,
    SpinningCircles,
    TailSpin,
    ThreeDots,
} from '@agney/react-loading';
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import { Message, useToaster } from "rsuite";

class InputErrors extends Component{
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
        var field_error_state = this.props.field_error_state
        var field_label = this.props.field_label

        return (
            <div>
                { // error -> required / invalid
                    field_error_state != undefined
                    ? <div> 
                        {
                            field_error_state === 'required'
                            ? <h6 style={{color: 'red'}}>{field_label} is required</h6>
                            : <h6 style={{color: 'red'}}>{field_label} is invalid</h6>
                        }
                    </div>
                    : <div></div>
                }
            </div>
        );
    }

};

export default withCookies(InputErrors);