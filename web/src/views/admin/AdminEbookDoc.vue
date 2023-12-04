<template>

   <!-- 表单工具栏 -->
   <div :style="{margin:'15px 20px 0'}">
    <a-input-search
      v-model:value="keyword"
      :style="{width:'30%', marginRight:'10px'}"
      size="large"
      placeholder="输入文档名称"
      @search="search"
      enter-button
    />
    <a-button type="primary" size="large" @click="showAddForm">新增</a-button>
   </div>
   <!-- row-key:表格行 key 的取值,表格子节点展开区分 -->
  <a-table :columns="columns" childrenColumnName="childs" :style="{margin:'10px'}"  
  :data-source="docs" :row-key="record => record.id">
 
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
  <!-- 文档表单 -->
  <a-modal
      ref="formRef"
      :title="docModal.title"
      okText="确定"
      cancelText="取消"
      v-model:open="editVisible"
      style="top: 20px"
      :confirm-loading="confirmLoading"
      @ok="handleEditOk"
    >
      <!-- 编辑表单 -->
      <a-form
        ref="docRef"
        :model="formDoc"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
      >
        <!-- 文档id -->
        <a-form-item label="编码" name="id" v-show="false">
          <a-input v-model:value="formDoc.id"/> 
        </a-form-item>
        <a-form-item label="名称" name="name">
          <a-input v-model:value="formDoc.name" />
        </a-form-item>
        <a-form-item label="电子书" name="ebook_name">
          <a-input v-model:value="formDoc.ebook_name" disabled />
        </a-form-item>
        <a-form-item label="父文档" name="parent_id">
          <!-- 文档下拉框 过滤掉当前文档-->
          <a-select
            ref="select"
            v-model:value="formDoc.parent_id"
            style="width: 120px"
            @change="tabLevel1"
          >
            <a-select-option value="">无</a-select-option>
            <a-select-option :value="c.id" v-for="c in docs"  :key="c.id" :disabled="c.id == formDoc.id">
            {{ c.name }}
          </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="排序" name="sort">
          <a-input-number v-model:value="formDoc.sort" />
        </a-form-item>
      </a-form>
  </a-modal>
</template>

<script lang="ts">
import { EditOutlined, DeleteOutlined,ExclamationCircleOutlined } from '@ant-design/icons-vue';
import type { TableColumnsType} from 'ant-design-vue';
import { Modal, message} from 'ant-design-vue';
import { defineComponent, onMounted, ref, getCurrentInstance, Ref } from 'vue';
import axios from 'axios';
import { h } from 'vue';
import { tools } from '@/assets/js/tools';
import { RuleObject } from 'ant-design-vue/es/form/interface';
// 文档信息定义
interface FormDoc {
  id: number;
  name: string;
  ebook_id: number;
  ebook_name: string;
  parent_id:number | string;
  sort: number | undefined;
  view_count: number | undefined;
  vote_count: number | undefined;
}

export default defineComponent({
  components: {
    EditOutlined,
    DeleteOutlined,
  },
  setup() {
    // 文档列表
    const docs = ref()//响应式对象
    const url = '/v1/docs'
    // 当前组件实例
    const {proxy} = getCurrentInstance()
    // 列表字段定义
    const columns = ref<TableColumnsType>([
      {
        title: '文档名称',
        dataIndex: 'name',//字段名
        key: 'name',
        resizable: true,
        width: 200,
        maxWidth: 300,
      },
      {
        title: '电子书',
        dataIndex: 'ebook_name',//字段名
        key: 'ebook_name',
      },
      {
        title: '编号',
        dataIndex: 'id',
        key: 'id',
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
        // 查询文档列表
        const params = {
          'ebookId': history.state.ebookId
        }
        console.log('history.state', params)
        // 发送请求， 查询文档信息
        handleQuery(params)
        
    })
    // 查询文档列表
    const handleQuery = function(params) {
        // 文档名称
        if( words != ''){
            params.name = words
          }
          axios.get(url, {params: params}).then(resp => {
            if(resp && resp.status == 200){
              // 获取响应结果
              const data = resp.data.content
              // 将文档列表转为树形结构
              docs.value = tools.array2tree(data, null)
            } 
            console.log('查询结果docs:'+docs);
            
         })
    }
    // ------------------电子书文档编辑弹窗
    // 提交表单
    const docRef = ref()
    // 电子书文档表单基础信息
    const docModal = ref({
        title: '文档新增',
        action: 'add'
      })
    const editVisible = ref(false)//编辑框是否可见
    const confirmLoading = ref<boolean>(false)//确定按钮 loading是否显示
    // UnwrapRef响应对象
    // ref对象定义 formDoc:Ref<FormDoc> = ref()
    // reactive对象定义 formDoc:FormDoc = reactive({对象})
    // reactive重新赋值对象，指向改变，新的对象不具备响应式能力
    let formDoc:Ref<FormDoc> = ref({
      'id': null,
      'name': '',
      'ebook_id': null,
      'ebook_name': '',
      'parent_id':null,
      'sort': null,
      'view_count': null,
      'vote_count': null
    });
    // 校验函数
    const checkName = async function(rule: RuleObject, value: string){
      // 校验文档名称
      if(value === ''){
        return Promise.reject('请输入名称');
      } else {
        return Promise.resolve();
      }
    }
    // 表单校验规则定义
    const rules = {
      name:[{ required: true, validator: checkName, trigger: 'change'}]
    }
    // 显示文档文档编辑窗口
    const showEditForm = function(docId){
      // 修改编辑框基本信息
      docModal.value = {
        title: '文档编辑',
        action: 'edit'
      }
      console.log('窗口标题'+ docModal.value.title);
      
      // 查询待编辑文档信息
      axios.get('/v1/docs/'+docId).then(resp =>{
        if (resp && resp.status == 200){
          formDoc.value = resp.data.content
          console.log('formDoc'+formDoc.value.id);
          
          // 显示编辑文档窗口
          editVisible.value = true
        }
      })
      // 显示文档文档表单信息
      console.log('选择编辑文档id：'+docId);
    }
    // 显示文档文档新增表单
    const showAddForm = function(){
      // 修改编辑框基本信息
      docModal.value = {
        title: '新增',
        action: 'add'
      }
      // 清空表单数据
      formDoc.value = {
        'id': null,
        'name': '',
        'ebook_id': null,
        'ebook_name': '',
        'parent_id':null,
        'sort': null,
        'view_count': null,
        'vote_count': null
      }
      editVisible.value = true
    }
    
    // 提交表单，显示编辑框
    const saveUrl = '/v1/docs/save'
    const addUrl = '/v1/docs/add'
    const handleEditOk = async function(){
      // 提交表单，校验规则
      docRef.value.validate().then(() => {
        console.info("-=-=-=-=通过");
        confirmLoading.value = true;
        //编辑窗口，保存文档文档
        console.log('保存文档信息：' + formDoc.value.name)
          //父文档选择为空处理
          if (formDoc.value.parent_id === ''){
            formDoc.value.parent_id=null
          }
        axios.post(docModal.value.action == 'add'?addUrl:saveUrl, formDoc.value).then((resp)=>{
          //处理保存文档文档返回结果, 显示结果框
          confirmLoading.value = false;
          if (resp && resp.status == 200){
            // 请求成功，隐藏表单
              editVisible.value = false;
              if(resp.data.success){
                message.success('文档文档信息保存成功！')
              }
            // 刷新文档文档列表
            handleQuery(undefined)
          }
        })
      })
      .catch((err) => {
            message.error('请完善文档信息，再提交')
      });
      
        
    }
    //选择父级文档 
    const tabLevel1 = function(value: string){
      console.log(`选择文档：${value}`);
      
    }

    // -----------------删除文档文档
    // const [modal, contextHolder] = Modal.useModal();
    const showDeleteForm = function(record){
      console.log('打开删除对话框')
      Modal.confirm({
        title: `确认删除文档?`,
        okText:'确定',
        cancelText:'取消',
        icon: h(ExclamationCircleOutlined),
        content: h('div', { style: 'color:red;' }, record.name),
        onOk() {
          // 发送删除请求
          console.log('OK，删除文档id:'+record.id);
          axios.delete('/v1/docs/'+record.id).then((resp) => {
            // 获取返回结果
            if (resp && resp.status == 200){
              // 请求成功，隐藏表单
              if(resp.data.success){
                message.success('文档删除成功！')
              }
              // 刷新文档列表
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
      docs,//文档列表
      columns,
      showEditForm,
      showAddForm,
      showDeleteForm,
      docModal,
      editVisible,
      confirmLoading,
      handleEditOk,
      docRef,//表单
      formDoc,//编辑表单数据
      rules,//校验规则
      tabLevel1,//选择父文档
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