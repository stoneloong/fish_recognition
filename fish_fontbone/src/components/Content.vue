<!-- 模板 -->
<template>
  <div id="Content">
    
    <el-dialog
      title="预测中"
      :visible.sync="dialogTableVisible"
      :show-close="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :close-on-click-modal="false"
      :center="true"
    >
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="text">请耐心等待</span>
    </el-dialog>
    <!-- 边框 -->
    <div id="aside">
      <!-- 管理员信息 -->
      <el-card class="box-card_1" style="width: 250px; height: 275px">
        <div slot="header" class="text_title">
          <span style="color: #800080" class="el-icon-info"> 管理员信息</span>
        </div>
        <div v-for="(value, name) in patient" :key="name" class="text">
          <h3 style="font-weight: normal">{{ name }}:{{ value }}</h3>
        </div>
      </el-card>
      <!-- 预测结果 -->
      <el-card 
        class="box-card_1" 
        body-style="padding: 15px 5px 15px 10px"
        style="width: 250px; height: 275px; margin-top: 50px"        
      >
        <div slot="header" class="text_title">
          <span style="color: #800080" class="el-icon-question"> 使用说明</span>
        </div>
        <div class="ext_title">
          <h3 style="font-weight: normal">
              <br>1、Demo
              <br>2、简单演示
              <br>3、不做商业用途
          </h3>
        </div>
      </el-card>
    </div>

    <!--主体部分-->
    <div id="image">
        <el-card
          class="box-card_2"
          style=" 
            border-radius: 8px;
            width: 800px;
            height: 450px;
            margin-bottom: -30px;
          "
        >
         <div slot="header" class="text_title">
          <span style="color: #800080" class="el-icon-picture"> 预测信息</span>
         </div>
          <div class="image_preview_1">
            <div
              v-loading="loading"
              element-loading-text="上传图片中"
              element-loading-spinner="el-icon-loading"
            >
              <el-image
                :src="url_1"
                class="image"
                :preview-src-list="srcList1"
                style="border-radius: 0 0 0 0"
              >
                <div slot="error">
                  <div slot="placeholder" class="item">
                    <el-button
                      v-show="showbutton"
                      type="primary"
                      icon="el-icon-upload"
                      class="button"
                      v-on:click="true_upload"
                    >
                      上传图片
                      <input
                        ref="upload"
                        style="display: none"
                        name="file"
                        type="file"
                        @change="update"
                      />
                    </el-button>
                  </div>
                </div>
              </el-image>
            </div>
            <!-- 原图文字 -->
            <div class="img_info" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 6px">原图</span>
            </div>
          </div>
          <!-- 语义分割图像 -->
          <div class="image_preview_2">
            <div
              v-loading="loading"
              element-loading-text="处理中,请耐心等待"
              element-loading-spinner="el-icon-loading"
            >
              <el-image
                :src="url_2"
                class="image"
                :preview-src-list="srcList2"
                style="border-radius: 3px 3px 0 0"
              >
                <div slot="error">
                  <div slot="placeholder" class="item">{{ wait_return }}</div>
                </div>
              </el-image>
            </div>
            <!-- 语义分割图像文字 -->
            <div class="img_info" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 4px">预测图像</span>
            </div>
          </div>
        </el-card>
        
        <el-card class="box-card_2" style="width: 800px; height: 130px; margin-top: 50px">
          <div slot="header" class="text_title">
            <span style="color: #800080" class="el-icon-success">预测结果为:{{ yucejieguo }}</span>    
          </div>
          <el-button
            style="margin-left: 290px"
            v-show="!showbutton"
            type="primary"
            icon="el-icon-upload"
            class="button"
            v-on:click="true_upload2"
            >
            重新上传图片
            <input
              ref="upload2"
              style="display: none"
              name="file"
              type="file"
              @change="update"
            />
          </el-button>
        </el-card>
      </div>
    </div>
</template>




<script>

import axios from "axios";

export default {
  name: "Content",
  data() {
    return {
      server_url: "http://127.0.0.1:5003",
      active: 0,
      centerDialogVisible: true,
      url_1: "",
      url_2: "",
      textarea: "",
      srcList1: [],
      srcList2: [],
      url: "",
      visible: false,
      wait_return: "等待返回",
      wait_upload: "等待上传",
      yucejieguo: "",
      loading: false,
      table: false,
      isNav: false,
      showbutton: true,
      percentage: 0,
      fullscreenLoading: false,
      opacitys: {
        opacity: 0,
      },
      dialogTableVisible: false,
      patient: {
        编号:   "001",
        用户名: "张三",
        权限: "管理员",
        公司: "xxxxxxxxxx"
      },
    };
  },
  created: function () {
    document.title = "海洋鱼类识别系统";
  },
  methods: {
    true_upload() {
      this.$refs.upload.click();
    },
    true_upload2() {
      this.$refs.upload2.click();
    },
    // 获得目标文件
    getObjectURL(file) {
      var url = null;
      if (window.createObjcectURL != undefined) {
        url = window.createOjcectURL(file);
      } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
      } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
      }
      return url;
    },
  
    // 上传文件
    update(e) {
      this.percentage = 0;
      this.dialogTableVisible = true;
      this.url_1 = "";
      this.url_2 = "";
      this.srcList1 = [];
      this.srcList2 = [];
      this.wait_return = "";
      this.wait_upload = "";
      this.fullscreenLoading = true;
      this.loading = true;
      this.showbutton = false;
      let file = e.target.files[0];
      this.url_1 = this.$options.methods.getObjectURL(file);
      let param = new FormData(); //创建form对象
      param.append("file", file, file.name); //通过append向form对象添加数据
      //console.log(param.get("file")); //FormData私有类对象，访问不到，可以通过get判断值是否传进去
      var timer = setInterval(() => {
        this.myFunc();
      }, 30);
      let config = {
        headers: { "Content-Type": "multipart/form-data" },
      }; //添加请求头
      axios
        .post(this.server_url + "/upload", param, config)
        .then((response) => {
          this.percentage = 100;
          clearInterval(timer);
          this.url_1 = response.data.image_url;
          this.srcList1.push(this.url_1);
          this.url_2 = response.data.draw_url;
          this.srcList2.push(this.url_2);
          this.fullscreenLoading = false;
          this.loading = false;
          this.dialogTableVisible = false;
          this.percentage = 0;
          this.yucejieguo = response.data.yucejieguo;
          this.notice();
        });
      },
    myFunc() {
      if (this.percentage + 33 < 99) {
        this.percentage = this.percentage + 33;
        this.percentage;
      } else {
        this.percentage = 99;
      }
    },
    notice() {
      this.$notify({
        title: "预测成功",
        message:"点击预测图像可查看大图",
        duration: 0,
        type: "success",
      })
    }
  }
}
</script>

<style>
.el-button {
  padding: 12px 20px !important;
}

#hello p {
  font-size: 15px !important;
  /*line-height: 25px;*/
}

.n1 .el-step__description {
  padding-right: 20%;
  font-size: 14px;
  line-height: 20px;
  /* font-weight: 400; */
}
</style>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.text {
  font-size: 14px;
}
.text_title{
  font-size: 20px;
}

.box-card_1 {
  width: 680px;
  height: 400px;
  border-radius: 8px;
  margin:20px;
}

.box-card_2 {
  width: 680px;
  height: 400px;
  border-radius: 8px;
  margin:20px;
}

.item {
  margin: 100px auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}

.button {
  padding: 10px 16px !important;
  background-color: #9521b9;
  
}
.button:hover{
  background-color: #ffffff;
  color: #9521b9;
}

.file {
  width: 200px;
  height: 130px;
  position: absolute;
  left: -20px;
  top: 0;
  z-index: 1;
  -moz-opacity: 0;
  -ms-opacity: 0;
  -webkit-opacity: 0;
  opacity: 0; /*css属性&mdash;&mdash;opcity不透明度，取值0-1*/
  filter: alpha(opacity=0);
  cursor: pointer;
}


.patient {
  margin: 50px auto;
  margin-bottom: 100px;
  /* margin-right: 100px; */
  background-color: #187aab;
  border-radius: 5px;
  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
  color: #fff;
  font-family: "Source Sans Pro", Verdana, sans-serif;
  font-size: 0.875rem;
  line-height: 1;
  padding: 0.75rem 1.5rem;
}

.image {
  width: 275px;
  height: 260px;
  background: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info {
  height: 30px;
  width: 275px;
  text-align: center;
  background-color: #9521b9;
  line-height: 30px;
}

.image_preview_1 {
  width: 250px;
  height: 290px;
  margin: 20px 60px;
  float: left;
}

.image_preview_2 {
  width: 250px;
  height: 290px;
  margin: 20px 460px;
}

#Content {
  width: 80%;
  height: 600px;
  background-color: #ffffff;
  margin: 15px auto;
  display: flex;
  min-width: 800px;
  margin-right: 30px;
  /* border: 1px solid #e4e7ed; */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#aside {
  width: 25%;
  height: 600px;
  background-color: #ffffff;
  margin-left: 25px;
  /* background-color: RGB(239, 249, 251); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */

}

#image {
  width: 60%;
  height: 80%;
  margin-left: 20px;
  margin-bottom: 50px;
  /* background-color: RGB(239, 249, 251); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#upload {
  position: relative;
  margin: 0px 0px;
}

</style>


