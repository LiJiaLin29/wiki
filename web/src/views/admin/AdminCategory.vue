<template>

   <!-- 表单工具栏 -->
   <div :style="{margin:'15px 20px 0'}">
    <a-input-search
      v-model:value="keyword"
      :style="{width:'30%', marginRight:'10px'}"
      size="large"
      placeholder="输入分类名称"
      @search="search"
      enter-button
    />
    <a-button type="primary" size="large" @click="showAddForm">新增</a-button>
   </div>
   <!-- row-key:表格行 key 的取值,表格子节点展开区分 -->
  <a-table :columns="columns" childrenColumnName="childs" :style="{margin:'10px'}"  
  :data-source="categorys" :row-key="record => record.id">
 
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'cover'">
        <img v-if="record.cover" :src="record.cover" class="img-cover"/>
      </template>
      <template v-else-if="column.key === 'action'">
        <span>
            <a-button @click="showEditForm(record.id)" type="primary" size="large">
                <template #icon><EditOutlined /></template>
                编辑
            </a-button>
          <a-divider type="vertical" />
          <a-button @click="showDeleteForm(record)" type="primary" danger size="large">
                <template #icon><DeleteOutlined /></template>
                删除
            </a-button>
        </span>
      </template>
    </template>
  </a-table>
  <!-- 分类表单 -->
  <a-modal
      ref="formRef"
      :title="categoryModal.title"
      okText="确定"
      cancelText="取消"
      v-model:open="editVisible"
      style="top: 20px"
      :confirm-loading="confirmLoading"
      @ok="handleEditOk"
    >
      <!-- 编辑表单 -->
      <a-form
        ref="categoryRef"
        :model="formCategory"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
      >
        <!-- 电子书id -->
        <a-form-item label="编码" name="id">
          <!-- 编辑表单展示时，编码字段禁用 -->
          <a-input v-model:value="formCategory.id" :disabled="categoryModal.action=='edit'"/> 
        </a-form-item>
        <a-form-item label="名称" name="name">
          <a-input v-model:value="formCategory.name" />
        </a-form-item>
        <a-form-item label="父分类" name="parent_id">
          <!-- 分类下拉框 过滤掉当前分类-->
          <a-select
            ref="select"
            v-model:value="formCategory.parent_id"
            style="width: 120px"
            @change="tabLevel1"
          >
            <a-select-option value="">无</a-select-option>
            <a-select-option :value="c.id" v-for="c in categorys"  :key="c.id" :disabled="c.id == formCategory.id">
            {{ c.name }}
          </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="排序" name="sort">
          <a-input-number v-model:value="formCategory.sort" />
        </a-form-item>
        <!-- <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
          <a-button type="primary" @click="onSubmit">Create</a-button>
          <a-button style="margin-left: 10px" @click="resetForm">Reset</a-button>
        </a-form-item> -->
      </a-form>
  </a-modal>
</template>
<!-- <script lang="ts" setup>
import { tools } from '@/assets/js/tools'
</script> -->

<script lang="ts">
import { EditOutlined, DeleteOutlined,ExclamationCircleOutlined } from '@ant-design/icons-vue';
import type { TableColumnsType} from 'ant-design-vue';
import { Modal, message} from 'ant-design-vue';
import { defineComponent, onMounted, ref, getCurrentInstance, UnwrapRef, reactive, Ref } from 'vue';
import axios from 'axios';
import { h } from 'vue';
import { tools } from '@/assets/js/tools';
import { RuleObject } from 'ant-design-vue/es/form/interface';
// 分类信息定义
interface FormCategory {
  id: number;
  name: string;
  parent_id:number | string;
  sort: number | undefined;
}

export default defineComponent({
  components: {
    EditOutlined,
    DeleteOutlined,
  },
  setup() {
    // 电子书列表
    const categorys = ref()//响应式对象
    const url = '/v1/categorys'
    // 当前组件实例
    const {proxy} = getCurrentInstance()
    // 列表字段定义
    const columns = ref<TableColumnsType>([
      {
        title: '编号',
        dataIndex: 'id',
        key: 'id',
        width: 200,
      },
      {
        title: '分类名称',
        dataIndex: 'name',//字段名
        key: 'name',
        resizable: true,
        width: 300,
        maxWidth: 400,
      },
      {
        title: '排序',
        key: 'sort',
        dataIndex: 'sort',
      },
      {
        title: '操作',
        key: 'action',
        width: 300
      },
    ]);
    //   生命周期钩子
    onMounted(()=>{
        // 查询电子书列表
        // 获取路径参数 字符串拼接
        let params = proxy.$route.query
        console.log('url路径参数：'+ params);
      
        // 发送请求， 查询电子书信息
        handleQuery(params)
        
    })
    // 查询分类列表
    const handleQuery = function(params) {
        // 电子书名称
        if( words != ''){
            params.name = words
          }
          axios.get(url, {params: params}).then(resp => {
            if(resp && resp.status == 200){
              // 获取响应结果
              const data = resp.data.content
              // 将分类列表转为树形结构
              categorys.value = tools.array2tree(data, null)
            } 
            console.log('查询结果categorys:'+categorys[0]);
            
         })
    }
    // ------------------电子书分类编辑弹窗
    // 电子书分类表单基础信息
    const categoryModal = ref({
        title: '分类新增',
        action: 'add'
      })
    const editVisible = ref(false)//编辑框是否可见
    const confirmLoading = ref<boolean>(false)//确定按钮 loading是否显示
    // UnwrapRef响应对象
    // ref对象定义 formCategory:Ref<FormCategory> = ref()
    // reactive对象定义 formCategory:FormCategory = reactive({对象})
    // reactive重新赋值对象，指向改变，新的对象不具备响应式能力
    let formCategory:Ref<FormCategory> = ref({
      'id': null,
      'name': '',
      'parent_id':null,
      'sort': null
    });//显示记录

    let checkCode = async (rule: RuleObject, value: string) => {
      // 分类编码规则，校验是否满足正整数
      if (value === '') {
        return Promise.reject('请输入编码');
      } else {
        if (!tools.checkIsPositive(formCategory.value.id)) {
          return Promise.reject('编码只能输入数字');
        }
        return Promise.resolve();
      }
    };
    // 表单校验规则定义
    const rules = {
      id:[
        { required: true, validator: checkCode, trigger: 'change'}
      ]
    }
    // 显示电子书分类编辑窗口
    const showEditForm = function(categoryId){
      // 修改编辑框基本信息
      categoryModal.value = {
        title: '分类编辑',
        action: 'edit'
      }
      console.log('窗口标题'+ categoryModal.value.title);
      
      // 查询待编辑电子书信息
      axios.get('/v1/categorys/'+categoryId).then(resp =>{
        if (resp && resp.status == 200){
          formCategory.value = resp.data.content
          console.log('formCategory'+formCategory.value.id);
          
          // 显示编辑电子书窗口
          editVisible.value = true
        }
      })
      // 显示电子书分类表单信息
      console.log('选择编辑分类id：'+categoryId);
    }
    // 显示电子书分类新增表单
    const showAddForm = function(){
      // 修改编辑框基本信息
      categoryModal.value = {
        title: '新增',
        action: 'add'
      }
      // 清空表单数据
      formCategory.value = {
        'id': null,
        'name': '',
        'parent_id':null,
        'sort': null
      }
      editVisible.value = true
    }
    // 提交表单，显示编辑框
    const saveUrl = '/v1/categorys/save'
    const addUrl = '/v1/categorys/add'
    const handleEditOk = async function(){
      
      confirmLoading.value = true;
      // setTimeout(() => {
      //   editVisible.value = false;
      //   confirmLoading.value = false;
      // }, 2000);
      //编辑窗口，保存电子书分类
      console.log('保存分类信息：' + formCategory.value.name)
        //父分类选择为空处理
        if (formCategory.value.parent_id === ''){
          formCategory.value.parent_id=null
        }
       await axios.post(categoryModal.value.action == 'add'?addUrl:saveUrl, formCategory.value).then((resp)=>{
        //处理保存电子书分类返回结果, 显示结果框
        confirmLoading.value = false;
        if (resp && resp.status == 200){
          // 请求成功，隐藏表单
            editVisible.value = false;
            if(resp.data.success){
              message.success('电子书分类信息保存成功！')
            }
          // 刷新电子书分类列表
          handleQuery(undefined)
         }
      })
        
    }
    //选择父级分类 
    const tabLevel1 = function(value: string){
      console.log(`选择分类：${value}`);
      
    }

    // -----------------删除电子书分类
    // const [modal, contextHolder] = Modal.useModal();
    const showDeleteForm = function(record){
      console.log('打开删除对话框')
      Modal.confirm({
        title: `确认删除分类?`,
        okText:'确定',
        cancelText:'取消',
        icon: h(ExclamationCircleOutlined),
        content: h('div', { style: 'color:red;' }, record.name),
        onOk() {
          // 发送删除请求
          console.log('OK，删除分类id:'+record.id);
          axios.delete('/v1/categorys/'+record.id).then((resp) => {
            // 获取返回结果
            if (resp && resp.status == 200){
              // 请求成功，隐藏表单
              if(resp.data.success){
                message.success('电子书删除成功！')
              }
              // 刷新电子书列表
              handleQuery(undefined)
            }
          })
        },
        onCancel() {
          console.log('Cancel');
        },
        class: 'test',
      });
    };
    // ------------------搜索功能
    // 点击搜索的有效搜索词
    const keyword = ref('')
    let words = ''
    // 点击搜索，更新搜索词
    const search = ()=>{
      words = keyword.value.trim()
      let params = {
        name: ''
      }
      if(words != ''){
        params.name = words
      }
      // 发送搜索请求
      handleQuery(params)
    }

    return {
      categorys,//分类列表
      columns,
      showEditForm,
      showAddForm,
      showDeleteForm,
      categoryModal,
      editVisible,
      confirmLoading,
      handleEditOk,
      formCategory,//编辑表单数据
      rules,//校验规则
      tabLevel1,//选择父分类
      handleResizeColumn: (w, col) => {
        col.width = w;
      },
      keyword,//搜索框
      search
    };
  },
});
</script>

<style scoped>
.img-cover {
    width: 48px;
    height: 48px;
}
</style>