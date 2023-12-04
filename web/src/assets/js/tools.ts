import { log } from "console"

// 常用的工具类
export const tools = {
    checkIsPositive: function (str){
        /** 
         * 检查参数是否为正整数
        */
        // 正整数
        const r = /^[1-9][0-9]*$/
        return r.test(str)
    },
    array2tree: function(array, parent_id:number){
        /**
         * 列表重构为树，从根部往下组装树
         * 获得元素的父节点，为子节点，拼接到结果列表中；
         * 不是子节点，
         */
        if(array.length==0){
            // 列表为空，返回原数组
            return array
        }
        let result = Array()
        for(let i in array){
            let v = array[i]
            // 判断当前元素是否为目标父节点parent_id的子元素
            if(v.parent_id === parent_id){
                //1.添加到列表中  
                result.push(v)
                // 2.将子节点存放到child字段中，继续从当前结果中找子节点
                const child = tools.array2tree(array, v.id)
                // console.log('子节点：'+child);
                
                if(child.length>0){
                    v.childs=child
                }
                // console.log('节点：'+v);
            }
        }
        return result
    }
  }
