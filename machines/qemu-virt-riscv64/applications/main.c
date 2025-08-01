/*
 * Copyright (c) 2006-2018, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 */

#include <rtthread.h>
#include <rthw.h>
#include <string.h>
#include "rust.h" // 包含 Rust 头文件
// #include <dfs_fs.h>

int main(void)
{
    rust_main();
    rt_kprintf("Hello RISC-V\n");
    return 0;
}
