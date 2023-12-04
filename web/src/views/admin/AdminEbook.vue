<template>

   <!-- 表单工具栏 -->
   <div :style="{margin:'15px 20px 0'}">
    <a-input-search
      v-model:value="keyword"
      :style="{width:'30%', marginRight:'10px'}"
      size="large"
      placeholder="输入电子书名称"
      @search="search"
      enter-button
    />
    <a-button type="primary" size="large" @click="showAddForm">新增</a-button>
   </div>
  <a-table :columns="columns" :style="{margin:'10px'}"  :data-source="ebooks" :pagination="pagination" @resizeColumn="handleResizeColumn">
 
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'cover'">
        <img v-if="record.cover" :src="record.cover" class="img-cover"/>
      </template>
      <template v-if="column.key === 'category'">
        <span>{{ record.category1_name }}/ {{ record.category2_name }}</span>
      </template>
      <template v-else-if="column.key === 'action'">
        <span>
            <RouterLink :to="{name: 'admin-ebook-docs', state: {ebookId: record.id}}">
            <a-button type="primary" size="large">
                  <template #icon><InboxOutlined /></template>
                  文档管理
              </a-button>
            </RouterLink>
            <a-divider type="vertical" />
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
  <!-- 电子书表单 -->
  <a-modal
      ref="formRef"
      :title="ebookModal.title"
      okText="确定"
      cancelText="取消"
      v-model:open="editVisible"
      style="top: 20px"
      :confirm-loading="confirmLoading"
      @ok="handleEditOk"
    >
      <!-- 编辑表单 -->
      <a-form
        ref="ebook"
        :model="formEbook"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
      >
        <!-- 电子书id -->
        <a-form-item name="id" v-show="false">
          <a-input v-model:value="formEbook.id" /> 
        </a-form-item>
        <a-form-item label="封面" name="cover">
          <a-input v-model:value="formEbook.cover" /> 
        </a-form-item>
        <a-form-item label="名称" name="name"
        :rules="[{ required: true, message: '请输入名称!' }]">
          <a-input v-model:value.trim="formEbook.name" />
        </a-form-item>
        <a-form-item label="分类" name="category"
        :rules="[{ required: true, message: '请选择分类!' }]">
        <a-cascader
          v-model:value="ebookCategoryValue"
          :options="categoryOptions"
          :field-names="{label:'name', value:'id', children:'childs'}"
          expand-trigger="hover"
          placeholder="请选择"
        />
        </a-form-item>
        <a-form-item label="描述" name="description" >
          <a-input v-model:value.trim="formEbook.description" placeholder="请输入描述信息"/>
        </a-form-item>
      </a-form>
  </a-modal>
</template>

<script lang="ts">
import { EditOutlined, DeleteOutlined,ExclamationCircleOutlined,InboxOutlined } from '@ant-design/icons-vue';
import type { TableColumnsType} from 'ant-design-vue';
import { Modal, message} from 'ant-design-vue';
import { defineComponent, onMounted, ref, getCurrentInstance } from 'vue';
import axios from 'axios';
import { h } from 'vue';
import { tools } from '@/assets/js/tools'
import { log } from 'console';

export default defineComponent({
  components: {
    EditOutlined,
    DeleteOutlined,
    InboxOutlined
  },
  setup() {
    // 电子书列表
    const ebooks = ref()//响应式对象
    const url = '/v1/ebooks'
    let categorys = {}//分类列表
    // 当前组件实例
    const {proxy} = getCurrentInstance()
    const pagination = ref({current: 1,
              pageSize: 5,
              total: null,
              showSizeChanger:true,//是否可以改变每页显示的条数
              pageSizeOptions: ['5','10','20'],//可选的每页条数
              showTotal: total => `共${total}条`,//总条数
              onChange: (current, pageSize)=> handleTabPage(current, pageSize)//页码、页数改变回调函数
            })
    
    const columns = ref<TableColumnsType>([
      {
        title: '封面',
        dataIndex: 'cover',
        key: 'cover',
        width: 100,
      },
      {
        title: '名称',
        dataIndex: 'name',//字段名
        key: 'name',
        resizable: true,
        width: 200,
        maxWidth: 280,
      },
      {
        title: '分类',
        key: 'category',
        dataIndex: 'category',
      },
      {
        title: '文档数',
        key: 'doc_count',
        dataIndex: 'doc_count',
      },
      {
        title: '阅读数',
        key: 'view_count',
        dataIndex: 'view_count',
      },
      {
        title: '点赞数',
        key: 'vote_count',
        dataIndex: 'vote_count',
      },
      {
        title: '操作',
        key: 'action',
        width: 400
      },
    ]);
    //   生命周期钩子
    onMounted(()=>{
        // 查询电子书列表
        // 获取路径参数 字符串拼接
        let params = proxy.$route.query
        console.log('url路径参数：'+ params);

        // 获取电子书分类列表
        axios.get('/v1/categorys').then(resp => {
            if(resp && resp.status == 200){
              // 获取响应结果
              const data = resp.data.content
              // 将分类列表转为树形结构
              categoryOptions.value = tools.array2tree(data, null)
              // 遍历，获取分类数组
              for(let i in data){
                const v = data[i]
                categorys[v.id] = v.name
              }
            } 
            // console.log('查询结果categorys:'+JSON.stringify(categorys));
            
         })
        // 发送请求， 查询电子书信息
        fetchEbookList(params)

    })
    // 点击页码， 重置分页器
    const handleTabPage = function(page, pageSize){
            const params = {
              page: page,
              pageSize: pageSize
            }
            handleQuery(params)
    }
    const handleQuery = function(params) {
        const data = fetchEbookList(params)
        //重置分页器,修改页码，总条数
        pagination.value.current = Number(params.page)
        pagination.value.pageSize = Number(params.pageSize)
        console.log('前端分页信息total：' + pagination.value.total);
        console.log('前端分页信息pageNo：' + pagination.value.current);
        console.log('前端分页信息pageSize：' + pagination.value.pageSize);
    }
    // 查询电子书列表
    const fetchEbookList = function(params) {
        // 未传入电子书查询参数，获取分页器信息
          if (params === undefined){
            params ={
              page: pagination.value.current,
              pageSize: pagination.value.pageSize
            }
          }
          // 电子书名称
          if( words != ''){
            params.name = words
          }
          let data:any//响应数据
          axios.get(url, {params: params}).then(resp => {
            if(resp && resp.status == 200){
              // 获取响应结果
              data = resp.data.content
              
              // 重置分页器: 总条数
              pagination.value.total = data.total

              //  修改电子书分类，显示名称
              const res = data.data
              for(let i=0; i<res.length; i++){
                  const element = res[i]
                  element.category1_name = categorys[element.category1_id]
                  element.category2_name = categorys[element.category2_id]
                  // console.log(categorys);
                  // console.log(element);
              }
              ebooks.value = res
            }  
         })    
    }
    // ------------------电子书编辑弹窗
    // 电子书表单基础信息
    const ebookModal = ref({
        title: '新增',
        action: 'add'
      })
    const editVisible = ref(false)//编辑框是否可见
    const confirmLoading = ref<boolean>(false)//确定按钮 loading是否显示
    const formEbook:any = ref({});//显示记录
    const ebookCategoryValue = ref();//分类级联框值
    const categoryOptions = ref(); //分类选项数组
    // 显示电子书编辑窗口
    const showEditForm = function(bookId){
      // 修改编辑框基本信息
      ebookModal.value = {
        title: '编辑',
        action: 'edit'
      }
      console.log('窗口标题'+ ebookModal.value.title);
      
      // 查询待编辑电子书信息
      axios.get('/v1/ebooks/'+bookId).then(resp =>{
        if (resp && resp.status == 200){
          formEbook.value = resp.data.content
          // 分类级联框赋值
          ebookCategoryValue.value = [formEbook.value.category1_id, formEbook.value.category2_id]
          // 显示编辑电子书窗口
          editVisible.value = true
        }
      })
      // 显示电子书表单信息
      console.log('选择编辑电子书id：'+bookId);
    }
    // 显示电子书新增表单
    const showAddForm = function(){
      // 修改编辑框基本信息
      ebookModal.value = {
        title: '新增',
        action: 'add'
      }
      // 清空表单数据
      formEbook.value = {}
      ebookCategoryValue.value = [null,null]
      editVisible.value = true
    }
    // 提交表单，显示编辑框
    const saveUrl = '/v1/ebooks/save'
    const addUrl = '/v1/ebooks/add'
    const handleEditOk = async function(){
      
      confirmLoading.value = true;
      // setTimeout(() => {
      //   editVisible.value = false;
      //   confirmLoading.value = false;
      // }, 2000);
      //编辑窗口，保存电子书
      // 分类级联控件拆解,判断是否选择值
      if(ebookCategoryValue.value!=null){
        console.log('分类已选择'+ebookCategoryValue.value);
        formEbook.value.category1_id = ebookCategoryValue.value[0]
        formEbook.value.category2_id = ebookCategoryValue.value[1]
      }else{
        console.log('分类未选择'+ebookCategoryValue.value);
        formEbook.value.category1_id = null
        formEbook.value.category2_id = null
      }
      console.log('保存的电子书信息：' + formEbook.value)
       await axios.post(ebookModal.value.action == 'add'?addUrl:saveUrl, formEbook.value).then((resp)=>{
        //处理保存电子书返回结果, 显示结果框
        confirmLoading.value = false;
        if (resp && resp.status == 200){
          // 请求成功，隐藏表单
            editVisible.value = false;
            if(resp.data.success){
              message.success('电子书信息保存成功！')
            }
          // 刷新电子书列表
          fetchEbookList(undefined)
         }
      })
        
    }

    // -----------------删除电子书
    // const [modal, contextHolder] = Modal.useModal();
    const showDeleteForm = function(record){
      console.log('打开删除对话框')
      Modal.confirm({
        title: `确认删除电子书?`,
        okText:'确定',
        cancelText:'取消',
        icon: h(ExclamationCircleOutlined),
        content: h('div', { style: 'color:red;' }, record.name),
        onOk() {
          // 发送删除请求
          console.log('OK，删除id:'+record.id);
          axios.delete('/v1/ebooks/'+record.id).then((resp) => {
            // 获取返回结果
            if (resp && resp.status == 200){
              // 请求成功，隐藏表单
              if(resp.data.success){
                message.success('电子书删除成功！')
              }
              // 刷新电子书列表
              fetchEbookList(undefined)
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
        page: 1,
        pageSize: 5,
        name: ''
      }
      if(words != ''){
        params.name = words
      }
      // 发送搜索请求
      handleQuery(params)
    }

    return {
      ebooks,
      columns,
      pagination,
      showEditForm,
      showAddForm,
      showDeleteForm,
      ebookModal,
      editVisible,
      confirmLoading,
      handleEditOk,
      formEbook,//编辑表单数据
      categoryOptions,//分类级联选项值
      ebookCategoryValue,//分类值
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