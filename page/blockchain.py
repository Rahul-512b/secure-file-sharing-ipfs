
from web3 import Web3

# connect to ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# check connection
print(web3.is_connected())

# paste your values here
contract_address = Web3.to_checksum_address("0x5edb86e6ee48e7815f4d1d0504bcc39eba0066e9")
abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_cid",
				"type": "string"
			}
		],
		"name": "uploadFile",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "files",
		"outputs": [
			{
				"internalType": "string",
				"name": "cid",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getFile",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]


contract = web3.eth.contract(address=contract_address, abi=abi)

account = web3.eth.accounts[0]

# send data
tx = contract.functions.uploadFile("QmPythonCID").transact({'from': account})

# read data
data = contract.functions.getFile(0).call()

print("Stored Data:", data)