# Blockchain-Chain-Custody
Cyberchase
Jaime Pesqueira - 1222168831
Kevin Doan - 1222041990
Adam Nguyen - 1222561561
Isaiah Nikodimos - 1213084962
The program is for Option 2, using Hyperledger. 
This is an application that creates and manages a blockchain to keep track of a chain of custody for evidence in forensic investigations.
To run our project, the following dependencies and software must be installed: Hyperledger Fabric binary and docker images (included in the fabric.zip file), Docker desktop, node, go, git, typescript, npm, and pycryptodome for hash functionality

1. Initialization: Upon starting, the program would check if the blockchain already exists by looking for an initial block. If not present, it would create an initial block containing predefined values, which acts as the genesis block for the blockchain.

2. Environment Variables: The program would use predefined environment variables for passwords associated with different roles (e.g., police, lawyer, analyst, etc.) and a hardcoded AES encryption key for securing IDs.

3. Adding Evidence: To add new evidence items to the blockchain, the program would take input such as the case ID and item ID. It would encrypt these IDs using AES ECB encryption with the provided key before storing them. The state of the newly added item is set to CHECKEDIN by default.

4. Changing Custody Status: The application would handle checkout and checkin actions, allowing users with the correct password to update the status of an evidence item to reflect its current custody status (checked out or checked in).

5. Removing Evidence: Users could remove an evidence item from active circulation within the blockchain. This action would be allowed only if the item is in a CHECKEDIN state and the user has the correct password.

6. Querying the Blockchain: The program would provide functionality to show all cases, items associated with a case, and the history of actions taken on an evidence item. To view detailed information, the correct password must be provided.

7. Verifying the Blockchain: There would be a verification process to ensure the integrity of the blockchain, checking for errors like mismatched hashes, duplicate entries, or improper state transitions.

8. Storing Data: All data within the blockchain would be stored in a binary format to maintain the integrity and security of the data.

Running the program:
1. Make sure to have docker open.
2. Run './bchoc_backup' to initialize the network and blockchain.
3. Run './bchoc' to run blockchain methods.

In case certain methods don't run:
1. cd fabric-samples/asset-transfer-basic/application-gateway-typescript/dist
2. node app.js [insert command] [options]

The zip file was too large for the github maximum filesize, so here is the link to download: https://drive.google.com/file/d/1Q6Y9QDUM6BmALPQYLXyFdmZY_swGyQIH/view?usp=sharing
