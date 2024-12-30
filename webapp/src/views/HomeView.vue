<template>
  <div class="wrapper">
      <div class="tiles">
          <div class="tile selected" title="Make Sale">
              <img src="/svg/shopping-basket.svg" alt="">
          </div>
          <div class="tile" title="Sales">
              <img src="/svg/wallet.svg" alt="">
          </div>
      </div>
      <div class="panel">
          <router-view></router-view>
      </div>
  </div>
</template>

<style lang="css" scoped>
  .wrapper {
    display: grid;
    grid-template-columns: 50px calc(100vw - 50px) ;
    background-color: #f2f1f2;
    height: 100vh;
    width: 100vw;
  }

  .tiles {
   height: 100vh;
   z-index: 10;
   background-color: white;
   border-right: solid 1.5px rgba(128, 128, 128, 0.301);
   width: 100%;
   cursor: pointer;
   transition: all 0.2s ease-in;
  }

  .tiles:hover {
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 3px 10px 0 rgba(58, 58, 58, 0.19);
  }

  .tile {
    margin-top: 10px;
    display: flex;
    position: relative;
    background-color: rgba(182, 182, 182, 0.86);
    width: 30px;
    height: 30px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 8px;
    transition: all 0.1s ease-in;
  }

  .tile.selected {
    background-color: rgba(243, 138, 27, 0.86);
  }

  .tile::before{
    content: "";
    display: flex;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    height: inherit;
    width: 0px;
    border-radius: 5px;
    background-color: rgba(128, 128, 128, 0.273);
    transition: all 0.1s ease-in;
  }

  .tile:hover::before{
    width: 100%;
  }

  .tile img {
    width: 20px;
    height: 20px;
    margin: auto;
  }
</style>

<script>
  export default {
      name: "SaleView"
  }
</script>