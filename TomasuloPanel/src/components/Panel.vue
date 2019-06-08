<template>
  <el-container>
    <el-aside width='400px'>
      <el-row id='title'>
        Tomasulo
      </el-row>
      <el-form>
        <el-form-item
          v-for="(value, key, index) in hdw_setting"
          :key="index"
          :label="value.label">
          <el-input-number v-model="value.num" :min="0" :precision="0"></el-input-number>
        </el-form-item>
      </el-form>
      <el-row>
        <el-upload
          class="upload-demo"
          action="/api/upload"
          :show-file-list="false"
          :disabled="isloading"
          :data="upload_setting">
          <el-button :type="upload_btn_status" round>Click to upload</el-button>
          <div slot="tip" class="el-upload__tip">NEL code file ('*.nel')</div>
        </el-upload>
      </el-row>
    </el-aside>
    <el-main v-loading="isloading">
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'Panel',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      isloading: false,
      hdw_setting: {
        ars: {
          num: 6,
          label: 'Num of Add RSs'
        },
        mrs: {
          num: 3,
          label: 'Num of Mult RSs'
        },
        lb: {
          num: 3,
          label: 'Num of Load Buffers'
        },
        add: {
          num: 3,
          label: 'Num of Add FUs'
        },
        mul: {
          num: 2,
          label: 'Num of Mul FUs'
        },
        ld: {
          num: 2,
          label: 'Num of Load FUs'
        },
        reg: {
          num: 32,
          label: 'Num of Used Regs'
        }
      }
    }
  },
  methods: {
    submitUpload () {
      this.isloading = true
      this.$refs.upload.submit()
      this.isloading = false
    }
  },
  computed: {
    upload_btn_status: function () {
      if (this.isloading) {
        return 'info'
      } else {
        return 'primary'
      }
    },
    upload_setting: function () {
      var res = {}
      for (var key in this.hdw_setting) {
        res[key] = this.hdw_setting[key].num
      }
      return res
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    /* line-height: 200px; */
}
.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 160px;
}
.el-container {
  height: 100vh;
}

#title {
  text-align: left;
  padding: 0px, 10px;
  padding-left: 10px;
  background-color: darkolivegreen;
  color: white;
  font-style: italic;
  font-size: 50px;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bolder;
}

.el-aside .el-form {
  margin-top: 20px;
}
.el-aside .el-form-item {
  padding-left: 30px;
  text-align: right;
}
.el-aside .el-form-item .el-input-number {
  margin-right: 20px;
}
</style>
