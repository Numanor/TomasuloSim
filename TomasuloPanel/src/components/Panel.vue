<template>
  <el-container>
    <el-header>Tomasulo</el-header>
    <el-container>
      <el-aside width='400px'>
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
        <el-table :data="instrs" id='code' height="270">
          <el-table-column
            prop="code"
            label="Code">
          </el-table-column>
          <el-table-column
            prop="issue"
            label="Issue"
            width="140">
          </el-table-column>
          <el-table-column
            prop="comp"
            label="ExecComp"
            width="140">
          </el-table-column>
          <el-table-column
            prop="wrtb"
            label="WriteBack"
            width="140">
          </el-table-column>
        </el-table>
        <el-row>
          <span>Input cycle to get corresponding info</span>
          <el-input-number v-model="cycle" :min="0" :max="maxcycle" :precision="0"></el-input-number>
        </el-row>
        <el-table :data="RSs" max-height="500">
          <el-table-column
            prop="name"
            label="NAME">
          </el-table-column>
          <el-table-column
            prop="busy"
            label="BUSY">
          </el-table-column>
          <el-table-column
            prop="op"
            label="OP">
          </el-table-column>
          <el-table-column
            prop="vj"
            label="Vj">
          </el-table-column>
          <el-table-column
            prop="vk"
            label="Vk">
          </el-table-column>
          <el-table-column
            prop="qj"
            label="Qj">
          </el-table-column>
          <el-table-column
            prop="qk"
            label="Qk">
          </el-table-column>
        </el-table>
        <el-row>
          <el-col :span="13">
            <el-table :data="LBs" max-height="400">
              <el-table-column
                prop="name"
                label="LOAD BUFFER">
              </el-table-column>
              <el-table-column
                prop="busy"
                label="BUSY"
                width="100">
              </el-table-column>
              <el-table-column
                prop="addr"
                label="ADDRESS"
                width="200">
              </el-table-column>
            </el-table>
          </el-col>
          <el-col :span="10">
            <el-table :data="REGs" max-height="400">
              <el-table-column
                prop="name"
                label="REG">
              </el-table-column>
              <el-table-column
                prop=status
                label="STATUS">
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'Panel',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      isloading: false,
      dataready: false,
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
      },
      instrs: [],
      cycle: 0,
      maxcycle: 0,
      REGs: [],
      LBs: [],
      RSs: []
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
.el-container {
  height: 100vh;
}

.el-header {
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

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
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

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  font-size: 20px;
}
.el-main .el-table {
  background: rgba(255, 255, 255, 0.3);
  font-size: 20px;
}
.el-main .el-row {
  margin: 10px 0px;
}
.el-main .el-row .el-col {
  /* background: #333; */
  /* height: 100px; */
  margin-right: 10px;
}
</style>
