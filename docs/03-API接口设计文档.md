# 企业ERP管理系统 - API接口设计文档

## 文档信息

| 项目名称 | 企业ERP管理系统 |
|---------|----------------|
| 文档版本 | v1.0 |
| 编写日期 | 2025-10-19 |
| API版本 | v1 |
| 基础URL | http://localhost:8000/api/v1 |

---

## 目录

1. [接口规范](#1-接口规范)
2. [认证授权接口](#2-认证授权接口)
3. [基础数据接口](#3-基础数据接口)
4. [库存管理接口](#4-库存管理接口)
5. [销售管理接口](#5-销售管理接口)
6. [采购管理接口](#6-采购管理接口)
7. [生产管理接口](#7-生产管理接口)
8. [财务管理接口](#8-财务管理接口)
9. [人力资源接口](#9-人力资源接口)
10. [错误码说明](#10-错误码说明)

---

## 1. 接口规范

### 1.1 RESTful设计原则

- **GET**：获取资源
- **POST**：创建资源
- **PUT**：更新资源（全量）
- **PATCH**：更新资源（部分）
- **DELETE**：删除资源

### 1.2 统一请求格式

#### 请求头

```http
Content-Type: application/json
Authorization: Bearer {access_token}
```

#### 分页参数

```json
{
  "page": 1,         // 页码，从1开始
  "page_size": 20,   // 每页数量
  "ordering": "-created_at"  // 排序字段，-表示降序
}
```

### 1.3 统一响应格式

#### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 响应数据
  }
}
```

#### 分页响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 100,        // 总记录数
    "next": "url",       // 下一页URL
    "previous": null,    // 上一页URL
    "results": []        // 当前页数据
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "请求参数错误",
  "errors": {
    "field_name": ["错误信息"]
  }
}
```

---

## 2. 认证授权接口

### 2.1 用户登录

**接口地址**：`POST /api/v1/auth/login/`

**请求参数**：

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应数据**：

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "admin",
      "real_name": "管理员",
      "avatar": "url",
      "dept_name": "技术部",
      "position_name": "系统管理员"
    }
  }
}
```

### 2.2 刷新Token

**接口地址**：`POST /api/v1/auth/token/refresh/`

**请求参数**：

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2.3 获取用户信息

**接口地址**：`GET /api/v1/auth/userinfo/`

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "admin",
    "real_name": "管理员",
    "avatar": "url",
    "email": "admin@example.com",
    "phone": "13800138000",
    "dept": {
      "id": 1,
      "dept_name": "技术部"
    },
    "position": {
      "id": 1,
      "position_name": "系统管理员"
    },
    "roles": [
      {
        "id": 1,
        "role_name": "超级管理员"
      }
    ],
    "permissions": ["user:add", "user:edit", "user:delete"]
  }
}
```

### 2.4 用户登出

**接口地址**：`POST /api/v1/auth/logout/`

**响应数据**：

```json
{
  "code": 200,
  "message": "退出登录成功"
}
```

### 2.5 修改密码

**接口地址**：`POST /api/v1/auth/change-password/`

**请求参数**：

```json
{
  "old_password": "admin123",
  "new_password": "admin456"
}
```

**响应数据**：

```json
{
  "code": 200,
  "message": "密码修改成功"
}
```

---

## 3. 基础数据接口

### 3.1 部门管理

#### 3.1.1 获取部门列表

**接口地址**：`GET /api/v1/foundation/departments/`

**请求参数**：

```
?dept_name=技术部    // 部门名称（模糊查询）
&status=1           // 状态
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "dept_code": "D001",
      "dept_name": "技术部",
      "parent_id": 0,
      "leader_id": 1,
      "leader_name": "张三",
      "phone": "010-12345678",
      "email": "tech@example.com",
      "sort_order": 1,
      "status": 1,
      "children": [
        {
          "id": 2,
          "dept_code": "D001-01",
          "dept_name": "研发组",
          "parent_id": 1
        }
      ]
    }
  ]
}
```

#### 3.1.2 获取部门详情

**接口地址**：`GET /api/v1/foundation/departments/{id}/`

#### 3.1.3 创建部门

**接口地址**：`POST /api/v1/foundation/departments/`

**请求参数**：

```json
{
  "parent_id": 0,
  "dept_code": "D001",
  "dept_name": "技术部",
  "dept_type": 2,
  "leader_id": 1,
  "phone": "010-12345678",
  "email": "tech@example.com",
  "sort_order": 1,
  "status": 1,
  "remark": "技术研发部门"
}
```

#### 3.1.4 更新部门

**接口地址**：`PUT /api/v1/foundation/departments/{id}/`

#### 3.1.5 删除部门

**接口地址**：`DELETE /api/v1/foundation/departments/{id}/`

---

### 3.2 用户管理

#### 3.2.1 获取用户列表

**接口地址**：`GET /api/v1/foundation/users/`

**请求参数**：

```
?username=admin     // 用户名
&real_name=张三     // 真实姓名
&dept_id=1          // 部门ID
&status=1           // 状态
&page=1
&page_size=20
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 100,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "username": "admin",
        "real_name": "管理员",
        "nickname": "超管",
        "avatar": "url",
        "email": "admin@example.com",
        "phone": "13800138000",
        "gender": 1,
        "dept": {
          "id": 1,
          "dept_name": "技术部"
        },
        "position": {
          "id": 1,
          "position_name": "系统管理员"
        },
        "status": 1,
        "last_login_at": "2025-10-19 12:00:00",
        "created_at": "2025-10-19 10:00:00"
      }
    ]
  }
}
```

#### 3.2.2 创建用户

**接口地址**：`POST /api/v1/foundation/users/`

**请求参数**：

```json
{
  "username": "zhangsan",
  "password": "123456",
  "real_name": "张三",
  "nickname": "小张",
  "email": "zhangsan@example.com",
  "phone": "13800138001",
  "gender": 1,
  "dept_id": 1,
  "position_id": 2,
  "role_ids": [2, 3],
  "status": 1
}
```

#### 3.2.3 更新用户

**接口地址**：`PUT /api/v1/foundation/users/{id}/`

#### 3.2.4 删除用户

**接口地址**：`DELETE /api/v1/foundation/users/{id}/`

#### 3.2.5 重置密码

**接口地址**：`POST /api/v1/foundation/users/{id}/reset-password/`

**请求参数**：

```json
{
  "new_password": "123456"
}
```

---

### 3.3 角色管理

#### 3.3.1 获取角色列表

**接口地址**：`GET /api/v1/foundation/roles/`

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "role_code": "admin",
      "role_name": "超级管理员",
      "role_type": 1,
      "data_scope": 1,
      "status": 1,
      "created_at": "2025-10-19 10:00:00"
    }
  ]
}
```

#### 3.3.2 创建角色

**接口地址**：`POST /api/v1/foundation/roles/`

**请求参数**：

```json
{
  "role_code": "sales_manager",
  "role_name": "销售经理",
  "role_type": 2,
  "data_scope": 2,
  "menu_ids": [1, 2, 3],
  "status": 1,
  "remark": "销售部门经理"
}
```

---

### 3.4 客户管理

#### 3.4.1 获取客户列表

**接口地址**：`GET /api/v1/foundation/customers/`

**请求参数**：

```
?customer_name=华为    // 客户名称
&customer_type=1      // 客户类型
&customer_level=1     // 客户等级
&status=1
&page=1
&page_size=20
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 50,
    "results": [
      {
        "id": 1,
        "customer_code": "C001",
        "customer_name": "华为技术有限公司",
        "customer_type": 1,
        "customer_type_display": "企业",
        "customer_level": 1,
        "customer_level_display": "重要客户",
        "industry": "通信设备",
        "contact_person": "李四",
        "contact_phone": "010-88888888",
        "contact_email": "lisi@huawei.com",
        "address": "深圳市龙岗区",
        "credit_limit": 1000000.00,
        "credit_days": 60,
        "status": 1,
        "created_at": "2025-10-19 10:00:00"
      }
    ]
  }
}
```

#### 3.4.2 创建客户

**接口地址**：`POST /api/v1/foundation/customers/`

**请求参数**：

```json
{
  "customer_code": "C001",
  "customer_name": "华为技术有限公司",
  "customer_type": 1,
  "customer_level": 1,
  "industry": "通信设备",
  "contact_person": "李四",
  "contact_phone": "010-88888888",
  "contact_email": "lisi@huawei.com",
  "address": "深圳市龙岗区",
  "credit_limit": 1000000.00,
  "credit_days": 60,
  "status": 1,
  "remark": "重要客户"
}
```

---

### 3.5 物料管理

#### 3.5.1 获取物料列表

**接口地址**：`GET /api/v1/foundation/materials/`

**请求参数**：

```
?material_name=芯片    // 物料名称
&material_code=M001    // 物料编码
&category_id=1         // 分类ID
&material_type=1       // 物料类型
&status=1
&page=1
&page_size=20
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 200,
    "results": [
      {
        "id": 1,
        "material_code": "M001",
        "material_name": "芯片-A001",
        "material_spec": "14nm",
        "category": {
          "id": 1,
          "category_name": "电子元器件"
        },
        "material_type": 1,
        "material_type_display": "原材料",
        "unit": "个",
        "price": 50.00,
        "min_stock": 100.0000,
        "max_stock": 1000.0000,
        "safety_stock": 200.0000,
        "barcode": "123456789",
        "status": 1,
        "created_at": "2025-10-19 10:00:00"
      }
    ]
  }
}
```

#### 3.5.2 创建物料

**接口地址**：`POST /api/v1/foundation/materials/`

**请求参数**：

```json
{
  "material_code": "M001",
  "material_name": "芯片-A001",
  "material_spec": "14nm",
  "category_id": 1,
  "material_type": 1,
  "unit": "个",
  "price": 50.00,
  "min_stock": 100.0000,
  "max_stock": 1000.0000,
  "safety_stock": 200.0000,
  "barcode": "123456789",
  "status": 1
}
```

---

## 4. 库存管理接口

### 4.1 库存查询

#### 4.1.1 获取库存列表

**接口地址**：`GET /api/v1/inventory/stocks/`

**请求参数**：

```
?warehouse_id=1       // 仓库ID
&material_id=1        // 物料ID
&batch_no=B001        // 批次号
&page=1
&page_size=20
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 150,
    "results": [
      {
        "id": 1,
        "warehouse": {
          "id": 1,
          "warehouse_name": "成品仓"
        },
        "material": {
          "id": 1,
          "material_code": "M001",
          "material_name": "芯片-A001",
          "unit": "个"
        },
        "batch_no": "B20251019001",
        "quantity": 500.0000,
        "available_qty": 450.0000,
        "locked_qty": 50.0000,
        "unit_cost": 48.50,
        "total_amount": 24250.00,
        "production_date": "2025-10-01",
        "expiry_date": "2026-10-01",
        "updated_at": "2025-10-19 10:00:00"
      }
    ]
  }
}
```

#### 4.1.2 库存预警

**接口地址**：`GET /api/v1/inventory/stocks/warning/`

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "warehouse_name": "原料仓",
      "material_code": "M001",
      "material_name": "芯片-A001",
      "current_qty": 50.0000,
      "safety_stock": 200.0000,
      "warning_type": "低于安全库存",
      "shortage_qty": 150.0000
    }
  ]
}
```

---

### 4.2 入库管理

#### 4.2.1 获取入库单列表

**接口地址**：`GET /api/v1/inventory/inbounds/`

**请求参数**：

```
?inbound_no=IN001      // 入库单号
&inbound_type=1        // 入库类型
&warehouse_id=1        // 仓库ID
&status=3              // 状态
&inbound_date_start=2025-10-01
&inbound_date_end=2025-10-31
&page=1
&page_size=20
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 80,
    "results": [
      {
        "id": 1,
        "inbound_no": "IN20251019001",
        "inbound_type": 1,
        "inbound_type_display": "采购入库",
        "warehouse": {
          "id": 1,
          "warehouse_name": "原料仓"
        },
        "source_doc_no": "PO20251019001",
        "inbound_date": "2025-10-19",
        "total_qty": 1000.0000,
        "total_amount": 50000.00,
        "status": 3,
        "status_display": "已审核",
        "audit_by_name": "张三",
        "audit_at": "2025-10-19 11:00:00",
        "created_by_name": "李四",
        "created_at": "2025-10-19 10:00:00"
      }
    ]
  }
}
```

#### 4.2.2 获取入库单详情

**接口地址**：`GET /api/v1/inventory/inbounds/{id}/`

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "inbound_no": "IN20251019001",
    "inbound_type": 1,
    "warehouse": {
      "id": 1,
      "warehouse_name": "原料仓"
    },
    "source_doc_no": "PO20251019001",
    "inbound_date": "2025-10-19",
    "total_qty": 1000.0000,
    "total_amount": 50000.00,
    "status": 3,
    "details": [
      {
        "id": 1,
        "material": {
          "id": 1,
          "material_code": "M001",
          "material_name": "芯片-A001",
          "unit": "个"
        },
        "batch_no": "B20251019001",
        "quantity": 500.0000,
        "unit_price": 50.00,
        "amount": 25000.00,
        "production_date": "2025-10-01",
        "expiry_date": "2026-10-01"
      }
    ],
    "created_by_name": "李四",
    "created_at": "2025-10-19 10:00:00",
    "remark": "采购入库"
  }
}
```

#### 4.2.3 创建入库单

**接口地址**：`POST /api/v1/inventory/inbounds/`

**请求参数**：

```json
{
  "inbound_type": 1,
  "warehouse_id": 1,
  "source_doc_no": "PO20251019001",
  "inbound_date": "2025-10-19",
  "details": [
    {
      "material_id": 1,
      "batch_no": "B20251019001",
      "quantity": 500.0000,
      "unit_price": 50.00,
      "production_date": "2025-10-01",
      "expiry_date": "2026-10-01"
    }
  ],
  "remark": "采购入库"
}
```

#### 4.2.4 审核入库单

**接口地址**：`POST /api/v1/inventory/inbounds/{id}/audit/`

**请求参数**：

```json
{
  "audit_result": true,  // true-通过，false-拒绝
  "audit_remark": "审核通过"
}
```

---

### 4.3 出库管理

#### 4.3.1 获取出库单列表

**接口地址**：`GET /api/v1/inventory/outbounds/`

#### 4.3.2 创建出库单

**接口地址**：`POST /api/v1/inventory/outbounds/`

**请求参数**：

```json
{
  "outbound_type": 1,
  "warehouse_id": 1,
  "source_doc_no": "SO20251019001",
  "outbound_date": "2025-10-19",
  "details": [
    {
      "material_id": 1,
      "batch_no": "B20251019001",
      "quantity": 100.0000
    }
  ],
  "remark": "销售出库"
}
```

---

## 5. 销售管理接口

### 5.1 销售订单管理

#### 5.1.1 获取销售订单列表

**接口地址**：`GET /api/v1/sales/orders/`

**请求参数**：

```
?order_no=SO001        // 订单号
&customer_id=1         // 客户ID
&status=3              // 状态
&order_date_start=2025-10-01
&order_date_end=2025-10-31
&page=1
&page_size=20
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 120,
    "results": [
      {
        "id": 1,
        "order_no": "SO20251019001",
        "customer": {
          "id": 1,
          "customer_name": "华为技术有限公司"
        },
        "order_date": "2025-10-19",
        "delivery_date": "2025-10-25",
        "total_qty": 200.0000,
        "total_amount": 100000.00,
        "discount_amount": 5000.00,
        "final_amount": 95000.00,
        "payment_method": 2,
        "payment_method_display": "转账",
        "status": 3,
        "status_display": "已审核",
        "created_by_name": "王五",
        "created_at": "2025-10-19 09:00:00"
      }
    ]
  }
}
```

#### 5.1.2 创建销售订单

**接口地址**：`POST /api/v1/sales/orders/`

**请求参数**：

```json
{
  "customer_id": 1,
  "order_date": "2025-10-19",
  "delivery_date": "2025-10-25",
  "payment_method": 2,
  "details": [
    {
      "material_id": 1,
      "quantity": 100.0000,
      "unit_price": 500.00,
      "discount_rate": 5.00,
      "delivery_date": "2025-10-25"
    }
  ],
  "remark": "重要订单"
}
```

#### 5.1.3 审核订单

**接口地址**：`POST /api/v1/sales/orders/{id}/audit/`

#### 5.1.4 取消订单

**接口地址**：`POST /api/v1/sales/orders/{id}/cancel/`

---

### 5.2 发货管理

#### 5.2.1 创建发货单

**接口地址**：`POST /api/v1/sales/deliveries/`

**请求参数**：

```json
{
  "order_id": 1,
  "warehouse_id": 1,
  "delivery_date": "2025-10-19",
  "logistics_company": "顺丰速运",
  "details": [
    {
      "order_detail_id": 1,
      "material_id": 1,
      "batch_no": "B20251019001",
      "quantity": 50.0000
    }
  ]
}
```

---

## 6. 采购管理接口

### 6.1 采购订单管理

#### 6.1.1 获取采购订单列表

**接口地址**：`GET /api/v1/procurement/orders/`

#### 6.1.2 创建采购订单

**接口地址**：`POST /api/v1/procurement/orders/`

**请求参数**：

```json
{
  "supplier_id": 1,
  "order_date": "2025-10-19",
  "delivery_date": "2025-10-25",
  "payment_method": 2,
  "details": [
    {
      "material_id": 1,
      "quantity": 1000.0000,
      "unit_price": 50.00,
      "delivery_date": "2025-10-25"
    }
  ],
  "remark": "紧急采购"
}
```

---

## 7. 生产管理接口

### 7.1 BOM管理

#### 7.1.1 获取BOM列表

**接口地址**：`GET /api/v1/production/boms/`

#### 7.1.2 创建BOM

**接口地址**：`POST /api/v1/production/boms/`

**请求参数**：

```json
{
  "bom_code": "BOM001",
  "product_id": 10,
  "bom_version": "1.0",
  "is_active": true,
  "effective_date": "2025-10-19",
  "details": [
    {
      "material_id": 1,
      "quantity": 2.0000,
      "loss_rate": 5.00,
      "sort_order": 1
    }
  ]
}
```

---

### 7.2 生产任务管理

#### 7.2.1 获取生产任务列表

**接口地址**：`GET /api/v1/production/tasks/`

#### 7.2.2 创建生产任务

**接口地址**：`POST /api/v1/production/tasks/`

**请求参数**：

```json
{
  "source_doc_no": "SO20251019001",
  "product_id": 10,
  "bom_id": 1,
  "plan_qty": 100.0000,
  "plan_start_date": "2025-10-20",
  "plan_end_date": "2025-10-25",
  "workshop_id": 1,
  "remark": "生产任务"
}
```

---

## 8. 财务管理接口

### 8.1 应收账款管理

#### 8.1.1 获取应收账款列表

**接口地址**：`GET /api/v1/finance/receivables/`

**请求参数**：

```
?customer_id=1
&status=1
&page=1
&page_size=20
```

**响应数据**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 60,
    "results": [
      {
        "id": 1,
        "bill_no": "AR20251019001",
        "customer": {
          "id": 1,
          "customer_name": "华为技术有限公司"
        },
        "order": {
          "id": 1,
          "order_no": "SO20251019001"
        },
        "bill_date": "2025-10-19",
        "receivable_amount": 95000.00,
        "received_amount": 50000.00,
        "balance_amount": 45000.00,
        "due_date": "2025-12-19",
        "status": 2,
        "status_display": "部分收款",
        "created_at": "2025-10-19 10:00:00"
      }
    ]
  }
}
```

---

## 9. 人力资源接口

### 9.1 员工管理

#### 9.1.1 获取员工列表

**接口地址**：`GET /api/v1/hrm/employees/`

#### 9.1.2 创建员工档案

**接口地址**：`POST /api/v1/hrm/employees/`

**请求参数**：

```json
{
  "employee_code": "E001",
  "real_name": "张三",
  "gender": 1,
  "id_card": "110101199001011234",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "dept_id": 1,
  "position_id": 2,
  "entry_date": "2025-10-01",
  "status": 1
}
```

---

### 9.2 考勤管理

#### 9.2.1 获取考勤记录

**接口地址**：`GET /api/v1/hrm/attendance/`

**请求参数**：

```
?employee_id=1
&attendance_date_start=2025-10-01
&attendance_date_end=2025-10-31
&page=1
&page_size=20
```

#### 9.2.2 打卡

**接口地址**：`POST /api/v1/hrm/attendance/clock/`

**请求参数**：

```json
{
  "clock_type": 1,  // 1-上班，2-下班
  "clock_time": "2025-10-19 09:00:00"
}
```

---

## 10. 错误码说明

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或Token失效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 409 | 资源冲突（如重复创建） |
| 422 | 数据验证失败 |
| 500 | 服务器内部错误 |
| 502 | 网关错误 |
| 503 | 服务不可用 |

---

**文档结束**
