// Smart Contract Addresses
export const VOTERS_ADDRESS = '0xAB5Bf724dd2723DD1a9FC493e57fA32C67e5833D'
export const ELECTIONS_ADDRESS = '0xd6D46EB703207D77eaA45482827F48eE6A50839E'
export const VOTES_ADDRESS = '0x1BD3D40506F1c3350be6588bD8ecf1DB205dbf56'
export const STAFF_ADDRESS = '0xb76d1F738C68fe67D4F78EaBaF57DB94B7d0d713'

// Smart Contract ABIs
export const VOTERS_ABI = [
    {
      "constant": true,
      "inputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "items",
      "outputs": [
        {
          "name": "id",
          "type": "uint256"
        },
        {
          "name": "firstname",
          "type": "string"
        },
        {
          "name": "lastname",
          "type": "string"
        },
        {
          "name": "addresss",
          "type": "string"
        },
        {
          "name": "id_number",
          "type": "string"
        },
        {
          "name": "phonenumber",
          "type": "string"
        },
        {
          "name": "gender",
          "type": "string"
        },
        {
          "name": "date_of_birth",
          "type": "string"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "currentCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "_firstname",
          "type": "string"
        },
        {
          "name": "_lastname",
          "type": "string"
        },
        {
          "name": "_addresss",
          "type": "string"
        },
        {
          "name": "_id_number",
          "type": "string"
        },
        {
          "name": "_phonenumber",
          "type": "string"
        },
        {
          "name": "_gender",
          "type": "string"
        },
        {
          "name": "_date_of_birth",
          "type": "string"
        }
      ],
      "name": "create",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "itemsCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    }
]
export const ELECTIONS_ABI = [
    {
      "constant": true,
      "inputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "items",
      "outputs": [
        {
          "name": "id",
          "type": "uint256"
        },
        {
          "name": "name",
          "type": "string"
        },
        {
          "name": "typee",
          "type": "string"
        },
        {
          "name": "election_date",
          "type": "string"
        },
        {
          "name": "contestants",
          "type": "string"
        },
        {
          "name": "election_end_date",
          "type": "string"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "currentCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "_name",
          "type": "string"
        },
        {
          "name": "_typee",
          "type": "string"
        },
        {
          "name": "_election_date",
          "type": "string"
        },
        {
          "name": "_contestants",
          "type": "string"
        },
        {
          "name": "_election_end_date",
          "type": "string"
        }
      ],
      "name": "create",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "itemsCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    }
]
export const VOTES_ABI = [
    {
      "constant": true,
      "inputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "items",
      "outputs": [
        {
          "name": "id",
          "type": "uint256"
        },
        {
          "name": "election_id",
          "type": "uint256"
        },
        {
          "name": "contestant",
          "type": "string"
        },
        {
          "name": "signature",
          "type": "bytes"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "currentCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "_election_id",
          "type": "uint256"
        },
        {
          "name": "_contestant",
          "type": "string"
        },
        {
          "name": "_signature",
          "type": "bytes"
        }
      ],
      "name": "create",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "itemsCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    }
]
export const STAFF_ABI = [
    {
      "constant": true,
      "inputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "items",
      "outputs": [
        {
          "name": "id",
          "type": "uint256"
        },
        {
          "name": "firstname",
          "type": "string"
        },
        {
          "name": "lastname",
          "type": "string"
        },
        {
          "name": "username",
          "type": "string"
        },
        {
          "name": "password",
          "type": "string"
        },
        {
          "name": "role",
          "type": "string"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "currentCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "_firstname",
          "type": "string"
        },
        {
          "name": "_lastname",
          "type": "string"
        },
        {
          "name": "_username",
          "type": "string"
        },
        {
          "name": "_password",
          "type": "string"
        }
      ],
      "name": "create",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "itemsCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    }
]