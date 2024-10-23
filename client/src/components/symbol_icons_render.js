// Modal.js
import React from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
import USD from '../images/usd_flag.png'
import EUR from '../images/eur_flag.png'
import JPY from '../images/jpy_flag.png'
import GBP from '../images/gbp_flag.png'
import CHF from '../images/chf_flag.png'
import ZAR from '../images/zar_flag.png'
import XAU from '../images/xau.png'
import CAD from '../images/cad_flag.png'
import AUD from '../images/aud_flag.png'
import NZD from '../images/nzd_flag.png'
import BTC from '../images/bitcoin.png'
import ETH from '../images/ethereum.png'
import LTC from '../images/lite_coin.png'
import XRP from '../images/xrp.png'
import Deriv from '../images/deriv.png'

const SymbolIconsRender = ({ symbol }) => {
    var base = ''; var quote = ''
    if(symbol === 'EURUSD'){ base = EUR; quote = USD }
    if(symbol === 'USDJPY'){ base = USD; quote = JPY }
    if(symbol === 'GBPUSD'){ base = GBP; quote = USD }
    if(symbol === 'USDCHF'){ base = USD; quote = CHF }
    if(symbol === 'USDZAR'){ base = USD; quote = ZAR }
    if(symbol === 'XAUUSD'){ base = XAU; quote = USD }
    if(symbol === 'GBPZAR'){ base = GBP; quote = ZAR }
    if(symbol === 'GBPCAD'){ base = GBP; quote = CAD }
    if(symbol === 'GBPAUD'){ base = GBP; quote = AUD }
    if(symbol === 'GBPJPY'){ base = GBP; quote = JPY }
    if(symbol === 'GBPNZD'){ base = GBP; quote = NZD }
    if(symbol === 'NZDCAD'){ base = NZD; quote = CAD }
    if(symbol === 'NZDUSD'){ base = NZD; quote = USD }
    if(symbol === 'AUDNZD'){ base = AUD; quote = NZD }
    if(symbol === 'AUDUSD'){ base = AUD; quote = USD }
    if(symbol === 'AUDCAD'){ base = AUD; quote = CAD }
    if(symbol === 'AUDJPY'){ base = AUD; quote = JPY }
    if(symbol === 'EURNZD'){ base = EUR; quote = NZD }
    if(symbol === 'EURGBP'){ base = EUR; quote = GBP }
    if(symbol === 'EURCAD'){ base = EUR; quote = CAD }
    if(symbol === 'EURAUD'){ base = EUR; quote = AUD }
    if(symbol === 'USDCAD'){ base = USD; quote = CAD }
    if(symbol === 'BTCUSD'){ base = BTC; quote = USD }
    if(symbol === 'ETHUSD'){ base = ETH; quote = USD }
    if(symbol === 'LTCUSD'){ base = LTC; quote = USD }
    if(symbol === 'XRPUSD'){ base = XRP; quote = USD }

    if (base === '' && quote === ''){ // for synthetic indices
        return <Row style={{margin: '0px'}}>
            <Col xs='6'>
                <img src={Deriv} style={{width: '30px', height: '30px'}} />
            </Col>
            <Col xs='6'>
                
            </Col>
        </Row>
    }else{ // for forex and crypto pairs
        return <Row style={{margin: '0px'}}>
            <Col xs='6'>
                <img src={base} style={{width: '30px', height: '30px'}} />
            </Col>
            <Col xs='6'>
                <img src={quote} style={{width: '30px', height: '30px'}} />
            </Col>
        </Row>
    }
};

export default SymbolIconsRender;
