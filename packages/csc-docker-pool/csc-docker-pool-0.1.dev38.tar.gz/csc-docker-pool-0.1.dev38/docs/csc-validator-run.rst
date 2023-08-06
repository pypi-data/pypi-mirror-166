Run a Validator
===============================================================================

Hardware
-------------------------------------------------------------------------------

..code-block::bash
  
  CPU: 16Core
  RAM: 32GB
  HDD: SSD 1TB

Initialize
-------------------------------------------------------------------------------

Refer to Run a Node

Create Validator Address
-------------------------------------------------------------------------------

You need to create an account that represents a validator's consensus key for 
block signatures. Use the following command to create a new account and set a 
password for that account:




..code-block::bash

  docker run --interactive \
    --volume $PWD:/root \
    --workdir /root \
    genzbank/cetd \
      account new \
      --datadir /root
    
  genz-cetd-pool \
    staking init \
      --name=main \
      --network=test

Start Validator Node
-------------------------------------------------------------------------------

Save keyfile password of validator account in file

..code-block::bash
  
  echo "your password" > password.txt



init 

genz-cetd -vv --force validator init \
    --name vascc \
    --relay ascc \
    --owner-wallet 0x1b0cceee915abc0d2c22be9f4c47c16233212aff \
    --reward-wallet 0xc787cdc0f4e50b92bf85c28bc2d7f423b7a09579 \
    --label GenZ \
    --description "GenZ CSC Full node" \
    --website "http://genz-bank.github.io" \
    --email "mostafa.barmshory@gmail.com" \
    --password 2625
    
Start mining

genz-cetd -vv validator start \
    --name vascc \
    --password 2625


genz-cetd-pool -vv validator stop \
    --name validator

..code-block::bash
  
  docker run --interactive \
    --volume $PWD:/root \
    --workdir /root \
    genzbank/cetd \
      --datadir /root \
      --unlock "0x8Db808CDB8606F66399E92FCc2b1b349c43671A2" 
      --password /root/password.txt  \
      --mine  \
      --allow-insecure-unlock






#--------------------------------------------------------------------------------
#----------------- GenZ Bank
#--------------------------------------------------------------------------------
validator: 0xeaff084e6da9afe8ecab4d85de940e7d3153296f
reward:   0x785f9c31920a827601f679ecee29a6fb47c31fc3


genz-cetd -vv --force validator init \
    --name vCZJ4270380 \
    --relay CZJ4270380 \
    --owner-wallet 0xeaff084e6da9afe8ecab4d85de940e7d3153296f \
    --reward-wallet 0x785f9c31920a827601f679ecee29a6fb47c31fc3 \
    --label GenZ \
    --description "GenZ CSC Full node" \
    --website "http://genz-bank.github.io" \
    --email "mostafa.barmshory@gmail.com" \
    --password 2625
    
Start mining

genz-cetd -vv validator start \
    --name vCZJ4270380 \
    --password 2625

genz-cetd -vv wallet stake \
    --name vCZJ4270380 \
    --relay CZJ4270380 \
    --from 0xeaff084e6da9afe8ecab4d85de940e7d3153296f \
    --value 10000000000000000000000 \
    --password 2625

# This command is ok, check with genz-cetd.
docker run --rm \
    -v "/home/maso/csc-working-dir/vCZJ4270380/:/root" \
    --network "csc" \
    ghcr.io/genz-bank/cetd \
    staking \
    --from 0xeaff084e6da9afe8ecab4d85de940e7d3153296f \
    --validator.address 0xeaff084e6da9afe8ecab4d85de940e7d3153296f \
    --validator.staking 10000000000000000000000 \
    --keystore /root/keystore/ \
    --node http://csc_relay_CZJ4270380_197031342:8545 \
    --password /root/password.txt 


docker run --rm \
    -v "/home/maso/csc-working-dir/vCZJ4270380/:/root" \
    --network "csc" \
    ghcr.io/genz-bank/cetd \
    --datadir /root \
    --unlock "0xeaff084e6da9afe8ecab4d85de940e7d3153296f" \
    --password /root/password.txt \
    --mine \
    --allow-insecure-unlock















genz-cetd wallet stake \
    --name validator \
    --relay relay \
    --from 0x3a4f8dfe9bb0e33a492487161a23187fef2db11e \
    --value 10000000000000000000000 \
    --password 2625











#----------- Local maso
genz-cetd -vv --force validator edit \
    --name validator \
    --relay relay \
    --owner-wallet 0x65ac59248995b86dfebd27b0707e24327a359ec4 \
    --reward-wallet 0x3a4f8dfe9bb0e33a492487161a23187fef2db11e \
    --label GenZ \
    --description "GenZ CSC Full node" \
    --website "http://genz-bank.github.io" \
    --email "mostafa.barmshory@gmail.com" \
    --password 1234


