import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Navbar, Nav, NavbarToggler, NavbarBrand, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupAddon,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
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
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import { Message, useToaster } from "rsuite";
import Logo from '../images/logo.png'

class NavBar extends Component{
    constructor(props) { 
        super(props);
        this.state = {
            isOpen: false,
            on_mobile: false
        };    
        
        this.HandleChange = (e) =>{
            this.setState({[e.target.name]: e.target.value});
        };

        this.toggle = () => {
            this.setState({
                isOpen: !this.state.isOpen
            });
        };
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
    }

    render() {
        return (
            <Navbar light expand="md" sticky='top' style={{backgroundColor: '#FFFFFF'}}>
                <NavbarBrand href="/" style={{marginBottom: '0px', height: '100px', backgroundColor: '', textAlign: 'left', width: '10%'}}>
                    <img src={Logo} style={{width: '100px'}} /> 
                </NavbarBrand>
                <NavbarToggler onClick={this.toggle} style={{backgroundColor: '#ffffff'}}/>
                <Collapse isOpen={this.state.isOpen} navbar>
                    <Nav className="ml-auto" navbar>
                        {
                            this.state.on_mobile == true
                            ? <>
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>  
                            </>
                            : <>
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>  
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>     
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>    
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>             
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>    
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>     
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>    
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>   
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem> 
                            </>
                        }   
                        <NavItem>
                            <NavLink href='/' style={{backgroundColor: 'inherit', border: 'none', color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                Home
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/how-it-works' style={{backgroundColor: 'inherit', border: 'none', color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                How it works
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/pricing' style={{backgroundColor: 'inherit', border: 'none', color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                Pricing
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/about-us' style={{backgroundColor: 'inherit', border: 'none', color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                About us
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/contact-us' style={{backgroundColor: 'inherit', border: 'none', color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                Contact us
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                    </Nav>
                </Collapse>
            </Navbar>
        );
    }

};

export default NavBar;