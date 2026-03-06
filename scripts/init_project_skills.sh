#!/usr/bin/env bash
#
# init_project_skills.sh - 交互式引入全局 Skills 到新项目
#
# 用法:
#   1. 在新项目目录下运行: bash /path/to/init_project_skills.sh
#   2. 或者添加到 PATH 后直接运行: init_project_skills.sh
#
# 功能:
#   - 扫描全局 skills 目录 (~/.claude/skills, ~/.trae/skills)
#   - 提供交互式多选界面
#   - 支持软链接或复制模式
#   - 自动创建 .agent/skills 或 .gemini/skills 目录
#

set -e

# ============ 配置 ============

# 全局 Skills 源目录
GLOBAL_SKILL_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.trae/skills"
)

# 默认目标目录（相对于当前项目）
DEFAULT_TARGET_DIRS=(
    ".trae/skills"
    ".claude/skills"
    ".agent/skills"
    ".gemini/skills"
)

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# 全局数组存储 skills 信息
SKILL_NAMES=()
SKILL_PATHS=()
SKILL_SELECTED=()

# ============ 辅助函数 ============

print_header() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}         ${BOLD}🚀 Skills 初始化工具 - 为新项目引入全局 Skills${NC}          ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${BLUE}────────────────────────────────────────────────────────────────────${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}────────────────────────────────────────────────────────────────────${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# 解析 SKILL.md 的 frontmatter
get_skill_info() {
    local skill_dir="$1"
    local skill_md="$skill_dir/SKILL.md"
    
    if [[ -f "$skill_md" ]]; then
        # 提取 name 和 description
        local name=$(sed -n '/^---$/,/^---$/p' "$skill_md" 2>/dev/null | grep -E "^name:" | head -1 | sed 's/name:[[:space:]]*//')
        local desc=$(sed -n '/^---$/,/^---$/p' "$skill_md" 2>/dev/null | grep -E "^description:" | head -1 | sed 's/description:[[:space:]]*//')
        
        # 如果没有 name，用目录名
        [[ -z "$name" ]] && name=$(basename "$skill_dir")
        # 如果没有 description，用默认值
        [[ -z "$desc" ]] && desc="No description"
        
        echo "$name|$desc"
    else
        echo "$(basename "$skill_dir")|No SKILL.md found"
    fi
}

# 检查是否是软链接
is_symlink() {
    [[ -L "$1" ]]
}

# 根据名称获取路径索引
get_skill_index() {
    local name="$1"
    for i in "${!SKILL_NAMES[@]}"; do
        if [[ "${SKILL_NAMES[$i]}" == "$name" ]]; then
            echo "$i"
            return
        fi
    done
    echo "-1"
}

# ============ 主要功能 ============

# 收集所有可用的 skills
collect_available_skills() {
    SKILL_NAMES=()
    SKILL_PATHS=()
    SKILL_SELECTED=()
    
    for global_dir in "${GLOBAL_SKILL_DIRS[@]}"; do
        if [[ ! -d "$global_dir" ]]; then
            continue
        fi
        
        for skill_item in "$global_dir"/*; do
            if [[ ! -d "$skill_item" ]]; then
                continue
            fi
            
            local skill_name=$(basename "$skill_item")
            
            # 如果是软链接，获取真实路径
            local real_path="$skill_item"
            if is_symlink "$skill_item"; then
                real_path=$(cd "$skill_item" 2>/dev/null && pwd -P) || real_path="$skill_item"
            fi
            
            # 检查是否已经添加过（去重）
            local already_added=false
            for existing in "${SKILL_NAMES[@]}"; do
                if [[ "$existing" == "$skill_name" ]]; then
                    already_added=true
                    break
                fi
            done
            
            if [[ "$already_added" == false ]]; then
                SKILL_NAMES+=("$skill_name")
                SKILL_PATHS+=("$real_path")
                SKILL_SELECTED+=(0)
            fi
        done
    done
}

# 显示 skills 列表 (交互式模式)
display_skills_list_interactive() {
    print_section "📦 可用的全局 Skills"
    echo ""
    
    for i in "${!SKILL_NAMES[@]}"; do
        local skill_name="${SKILL_NAMES[$i]}"
        local source_path="${SKILL_PATHS[$i]}"
        local info=$(get_skill_info "$source_path")
        local desc=$(echo "$info" | cut -d'|' -f2 | cut -c1-50)
        
        # 检查是否已选中
        local selected_marker=" "
        if [[ "${SKILL_SELECTED[$i]}" == "1" ]]; then
            selected_marker="${GREEN}✓${NC}"
        fi
        
        # 显示来源标记
        local source_tag=""
        if [[ "$source_path" == *"/.claude/"* ]]; then
            source_tag="${MAGENTA}[claude]${NC}"
        elif [[ "$source_path" == *"/.trae/"* ]]; then
            source_tag="${BLUE}[trae]${NC}"
        fi
        
        printf "  ${BOLD}%2d${NC}. [%b] %-25s %b %s\n" "$((i+1))" "$selected_marker" "$skill_name" "$source_tag" "$desc"
    done
    echo ""
}

# 显示 skills 列表 (普通模式)
show_available_skills() {
    print_section "📦 可用的全局 Skills (${#SKILL_NAMES[@]} 个)"
    echo ""
    
    for i in "${!SKILL_NAMES[@]}"; do
        local skill_name="${SKILL_NAMES[$i]}"
        local source_path="${SKILL_PATHS[$i]}"
        local info=$(get_skill_info "$source_path")
        local desc=$(echo "$info" | cut -d'|' -f2 | cut -c1-55)
        
        # 显示来源标记
        local source_tag=""
        if [[ "$source_path" == *"/.claude/"* ]]; then
            source_tag="${MAGENTA}[claude]${NC}"
        elif [[ "$source_path" == *"/.trae/"* ]]; then
            source_tag="${BLUE}[trae]${NC}"
        fi
        
        printf "  ${BOLD}%2d${NC}. %-28s %b %s\n" "$((i+1))" "$skill_name" "$source_tag" "$desc"
    done
    echo ""
}

# 切换指定索引的选择状态
toggle_selection() {
    local idx=$1
    if [[ $idx -ge 0 ]] && [[ $idx -lt ${#SKILL_NAMES[@]} ]]; then
        if [[ "${SKILL_SELECTED[$idx]}" == "1" ]]; then
            SKILL_SELECTED[$idx]=0
        else
            SKILL_SELECTED[$idx]=1
        fi
    fi
}

# 解析并处理选择输入（支持 "9-11, 14-15, 20-24" 这种格式）
parse_selection_input() {
    local input="$1"
    
    # 移除所有空格，用逗号分隔
    input=$(echo "$input" | tr -d ' ')
    
    # 用逗号分隔成多个部分
    IFS=',' read -ra parts <<< "$input"
    
    for part in "${parts[@]}"; do
        if [[ -z "$part" ]]; then
            continue
        fi
        
        if [[ "$part" == *-* ]]; then
            # 范围选择 (如: 9-11)
            local start=$(echo "$part" | cut -d'-' -f1)
            local end=$(echo "$part" | cut -d'-' -f2)
            if [[ "$start" =~ ^[0-9]+$ ]] && [[ "$end" =~ ^[0-9]+$ ]]; then
                for ((i=start; i<=end; i++)); do
                    toggle_selection $((i-1))
                done
            fi
        elif [[ "$part" =~ ^[0-9]+$ ]]; then
            # 单个数字
            toggle_selection $((part-1))
        fi
    done
}

# 交互式选择 skills
interactive_select() {
    while true; do
        clear
        print_header
        display_skills_list_interactive
        
        local selected_count=0
        for val in "${SKILL_SELECTED[@]}"; do
            [[ "$val" == "1" ]] && ((selected_count++)) || true
        done
        
        echo -e "${CYAN}已选择: ${BOLD}$selected_count${NC}${CYAN} 个 Skills${NC}"
        echo ""
        echo -e "输入操作指令:"
        echo -e "  ${BOLD}数字${NC}       - 切换选择状态 (如: 1, 2, 3)"
        echo -e "  ${BOLD}范围${NC}       - 批量选择 (如: 1-5, 9-11, 14-15)"
        echo -e "  ${BOLD}混合${NC}       - 组合输入 (如: 1, 3-5, 8, 10-12)"
        echo -e "  ${BOLD}a / all${NC}   - 全选"
        echo -e "  ${BOLD}n / none${NC}  - 取消全选"
        echo -e "  ${BOLD}d / done${NC}  - 确认选择并继续"
        echo -e "  ${BOLD}q / quit${NC}  - 退出"
        echo ""
        read -p "$(echo -e ${YELLOW}请输入: ${NC})" input
        
        case "$input" in
            a|all)
                for i in "${!SKILL_SELECTED[@]}"; do
                    SKILL_SELECTED[$i]=1
                done
                ;;
            n|none)
                for i in "${!SKILL_SELECTED[@]}"; do
                    SKILL_SELECTED[$i]=0
                done
                ;;
            d|done)
                break
                ;;
            q|quit)
                echo ""
                print_info "已取消操作"
                exit 0
                ;;
            *)
                # 解析混合输入（数字、范围、逗号分隔）
                parse_selection_input "$input"
                ;;
        esac
    done
}

# 选择目标目录
select_target_directory() {
    print_section "📁 选择目标目录"
    echo ""
    echo -e "当前项目目录: ${BOLD}$(pwd)${NC}"
    echo ""
    echo "选择 Skills 安装位置:"
    echo ""
    
    local idx=1
    for dir in "${DEFAULT_TARGET_DIRS[@]}"; do
        local status=""
        if [[ -d "$dir" ]]; then
            status="${GREEN}(已存在)${NC}"
        fi
        printf "  ${BOLD}%d${NC}. %-20s %b\n" "$idx" "$dir" "$status"
        ((idx++))
    done
    echo -e "  ${BOLD}$idx${NC}. 自定义路径..."
    echo ""
    
    read -p "$(echo -e ${YELLOW}请选择 [1]: ${NC})" choice
    choice=${choice:-1}
    
    if [[ "$choice" == "$idx" ]]; then
        read -p "$(echo -e ${YELLOW}输入自定义路径: ${NC})" custom_path
        echo "$custom_path"
    elif [[ $choice -ge 1 ]] && [[ $choice -lt $idx ]]; then
        echo "${DEFAULT_TARGET_DIRS[$((choice-1))]}"
    else
        echo "${DEFAULT_TARGET_DIRS[0]}"
    fi
}

# 选择安装模式
select_install_mode() {
    print_section "🔧 选择安装模式"
    echo ""
    echo "选择如何引入 Skills:"
    echo ""
    echo -e "  ${BOLD}1${NC}. ${GREEN}软链接${NC} (推荐) - 创建符号链接，自动同步更新"
    echo -e "  ${BOLD}2${NC}. ${BLUE}复制${NC}         - 完整复制，独立管理"
    echo ""
    
    read -p "$(echo -e ${YELLOW}请选择 [1]: ${NC})" mode
    mode=${mode:-1}
    
    case "$mode" in
        2) echo "copy" ;;
        *) echo "symlink" ;;
    esac
}

# 执行安装 (交互式模式)
perform_install() {
    local target_dir="$1"
    local mode="$2"
    
    print_section "⚡ 执行安装"
    echo ""
    
    # 创建目标目录
    if [[ ! -d "$target_dir" ]]; then
        mkdir -p "$target_dir"
        print_success "创建目录: $target_dir"
    fi
    
    local installed_count=0
    local skipped_count=0
    
    for i in "${!SKILL_NAMES[@]}"; do
        if [[ "${SKILL_SELECTED[$i]}" != "1" ]]; then
            continue
        fi
        
        local skill_name="${SKILL_NAMES[$i]}"
        local source_path="${SKILL_PATHS[$i]}"
        local target_path="$target_dir/$skill_name"
        
        # 检查是否已存在
        if [[ -e "$target_path" ]] || [[ -L "$target_path" ]]; then
            print_warning "跳过 $skill_name (已存在)"
            ((skipped_count++))
            continue
        fi
        
        if [[ "$mode" == "symlink" ]]; then
            ln -s "$source_path" "$target_path"
            print_success "链接 $skill_name -> $source_path"
        else
            cp -r "$source_path" "$target_path"
            print_success "复制 $skill_name"
        fi
        
        ((installed_count++))
    done
    
    echo ""
    print_section "📊 安装完成"
    echo ""
    echo -e "  安装: ${GREEN}${BOLD}$installed_count${NC} 个 Skills"
    echo -e "  跳过: ${YELLOW}${BOLD}$skipped_count${NC} 个 (已存在)"
    echo -e "  位置: ${BOLD}$target_dir${NC}"
    echo ""
}

# 显示使用提示
show_usage_tips() {
    local target_dir="$1"
    
    print_section "💡 使用提示"
    echo ""
    echo "已安装的 Skills 可以通过以下方式使用:"
    echo ""
    echo -e "  1. ${BOLD}Gemini${NC} - 在 .gemini/settings.json 中配置 skills 路径"
    echo -e "  2. ${BOLD}Claude${NC} - 将目录添加到 .claude/skills"
    echo -e "  3. ${BOLD}Trae${NC}   - 自动识别 .trae/skills 目录"
    echo ""
    echo -e "查看已安装的 Skills:"
    echo -e "  ${CYAN}ls -la $target_dir${NC}"
    echo ""
}

# ============ 帮助和列表显示 ============

show_help() {
    print_header
    echo -e "${BOLD}用法:${NC}"
    echo "  init_project_skills.sh [选项] [skill名称...]"
    echo ""
    echo -e "${BOLD}选项:${NC}"
    echo "  -h, --help          显示此帮助信息"
    echo "  -l, --list          仅列出可用的 Skills"
    echo "  -i, --interactive   进入交互式选择模式"
    echo "  -t, --target DIR    指定目标目录 (默认: .agent/skills)"
    echo "  -c, --copy          使用复制模式而非软链接"
    echo "  -a, --all           安装所有可用的 Skills"
    echo ""
    echo -e "${BOLD}示例:${NC}"
    echo "  init_project_skills.sh                    # 显示帮助和可用 Skills"
    echo "  init_project_skills.sh -i                 # 进入交互式选择模式"
    echo "  init_project_skills.sh -l                 # 仅列出可用 Skills"
    echo "  init_project_skills.sh skill-manager      # 安装指定的 skill"
    echo "  init_project_skills.sh -a -t .trae/skills # 安装全部到指定目录"
    echo "  init_project_skills.sh 'git-*' 'prompt-*' # 使用通配符安装匹配的 skills"
    echo ""
}

# 快速安装指定的 skills
quick_install() {
    local target_dir="$1"
    local mode="$2"
    shift 2
    local skill_patterns=("$@")
    
    # 创建目标目录
    if [[ ! -d "$target_dir" ]]; then
        mkdir -p "$target_dir"
        print_success "创建目录: $target_dir"
    fi
    
    local installed_count=0
    local skipped_count=0
    local not_found_count=0
    
    for pattern in "${skill_patterns[@]}"; do
        local found=false
        for i in "${!SKILL_NAMES[@]}"; do
            local skill_name="${SKILL_NAMES[$i]}"
            # 支持通配符匹配
            if [[ "$skill_name" == $pattern ]]; then
                found=true
                local source_path="${SKILL_PATHS[$i]}"
                local target_path="$target_dir/$skill_name"
                
                if [[ -e "$target_path" ]] || [[ -L "$target_path" ]]; then
                    print_warning "跳过 $skill_name (已存在)"
                    ((skipped_count++))
                    continue
                fi
                
                if [[ "$mode" == "symlink" ]]; then
                    ln -s "$source_path" "$target_path"
                    print_success "链接 $skill_name"
                else
                    cp -r "$source_path" "$target_path"
                    print_success "复制 $skill_name"
                fi
                ((installed_count++))
            fi
        done
        
        if [[ "$found" == false ]] && [[ "$pattern" != *"*"* ]]; then
            print_error "未找到: $pattern"
            ((not_found_count++))
        fi
    done
    
    echo ""
    print_section "📊 安装完成"
    echo ""
    echo -e "  安装: ${GREEN}${BOLD}$installed_count${NC} 个 Skills"
    [[ $skipped_count -gt 0 ]] && echo -e "  跳过: ${YELLOW}${BOLD}$skipped_count${NC} 个 (已存在)"
    [[ $not_found_count -gt 0 ]] && echo -e "  未找到: ${RED}${BOLD}$not_found_count${NC} 个"
    echo -e "  位置: ${BOLD}$target_dir${NC}"
    echo ""
}

# ============ 主函数 ============

main() {
    # 解析参数
    local interactive_mode=false
    local list_only=false
    local install_all=false
    local copy_mode=false
    local target_dir=".trae/skills"
    local skill_args=()
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -l|--list)
                list_only=true
                shift
                ;;
            -i|--interactive)
                interactive_mode=true
                shift
                ;;
            -a|--all)
                install_all=true
                shift
                ;;
            -c|--copy)
                copy_mode=true
                shift
                ;;
            -t|--target)
                target_dir="$2"
                shift 2
                ;;
            -*)
                print_error "未知选项: $1"
                echo "使用 -h 查看帮助"
                exit 1
                ;;
            *)
                skill_args+=("$1")
                shift
                ;;
        esac
    done
    
    local install_mode="symlink"
    [[ "$copy_mode" == true ]] && install_mode="copy"
    
    # 收集可用 skills
    collect_available_skills
    
    if [[ ${#SKILL_NAMES[@]} -eq 0 ]]; then
        print_header
        print_error "未找到任何全局 Skills"
        echo ""
        echo "请确保以下目录存在并包含 Skills:"
        for dir in "${GLOBAL_SKILL_DIRS[@]}"; do
            echo "  - $dir"
        done
        exit 1
    fi
    
    # 仅列出模式
    if [[ "$list_only" == true ]]; then
        print_header
        show_available_skills
        exit 0
    fi
    
    # 如果没有任何参数，显示帮助和列表，并提供快速选择
    if [[ "$interactive_mode" == false ]] && [[ "$install_all" == false ]] && [[ ${#skill_args[@]} -eq 0 ]]; then
        show_help
        show_available_skills
        
        echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"
        echo -e "${CYAN}  🚀 快速安装${NC}"
        echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"
        echo ""
        echo -e "目标目录: ${BOLD}$target_dir${NC}  ${YELLOW}(使用 -t 选项修改)${NC}"
        echo ""
        echo -e "输入要安装的 Skills (直接回车退出):"
        echo -e "  ${BOLD}数字${NC}      - 安装单个 (如: 1)"
        echo -e "  ${BOLD}范围${NC}      - 批量安装 (如: 1-5)"
        echo -e "  ${BOLD}多个${NC}      - 用空格或逗号分隔 (如: 1 3 5 或 1,3,5)"
        echo -e "  ${BOLD}名称${NC}      - 直接输入名称 (如: skill-manager)"
        echo -e "  ${BOLD}i${NC}         - 进入交互式选择 (可选择目录)"
        echo -e "  ${BOLD}q${NC}         - 退出"
        echo ""
        read -p "$(echo -e ${YELLOW}请输入: ${NC})" quick_input
        
        # 空输入则退出
        if [[ -z "$quick_input" ]] || [[ "$quick_input" == "q" ]]; then
            exit 0
        fi
        
        # 进入交互式模式
        if [[ "$quick_input" == "i" ]]; then
            interactive_mode=true
        else
            # 解析输入
            local input_items=()
            for item in $quick_input; do
                if [[ "$item" == *-* ]] && [[ "$item" =~ ^[0-9]+-[0-9]+$ ]]; then
                    # 范围选择
                    local start=$(echo "$item" | cut -d'-' -f1)
                    local end=$(echo "$item" | cut -d'-' -f2)
                    for ((i=start; i<=end; i++)); do
                        local idx=$((i-1))
                        if [[ $idx -ge 0 ]] && [[ $idx -lt ${#SKILL_NAMES[@]} ]]; then
                            input_items+=("${SKILL_NAMES[$idx]}")
                        fi
                    done
                elif [[ "$item" =~ ^[0-9]+$ ]]; then
                    # 数字索引
                    local idx=$((item-1))
                    if [[ $idx -ge 0 ]] && [[ $idx -lt ${#SKILL_NAMES[@]} ]]; then
                        input_items+=("${SKILL_NAMES[$idx]}")
                    else
                        print_error "无效索引: $item"
                    fi
                else
                    # 名称
                    input_items+=("$item")
                fi
            done
            
            if [[ ${#input_items[@]} -gt 0 ]]; then
                echo ""
                quick_install "$target_dir" "$install_mode" "${input_items[@]}"
                exit 0
            fi
        fi
    fi
    
    # 安装所有
    if [[ "$install_all" == true ]]; then
        print_header
        print_info "安装所有 Skills 到 $target_dir"
        echo ""
        
        # 将所有 skill 添加到参数
        for skill_name in "${SKILL_NAMES[@]}"; do
            skill_args+=("$skill_name")
        done
    fi
    
    # 快速安装指定的 skills
    if [[ ${#skill_args[@]} -gt 0 ]]; then
        print_header
        quick_install "$target_dir" "$install_mode" "${skill_args[@]}"
        exit 0
    fi
    
    # 交互式模式
    if [[ "$interactive_mode" == true ]]; then
        # 检查是否在项目目录中
        if [[ ! -f "package.json" ]] && [[ ! -f "pyproject.toml" ]] && [[ ! -d ".git" ]]; then
            print_warning "当前目录看起来不像是一个项目根目录"
            read -p "$(echo -e ${YELLOW}是否继续? [y/N]: ${NC})" confirm
            if [[ "$confirm" != "y" ]] && [[ "$confirm" != "Y" ]]; then
                exit 0
            fi
        fi
        
        # 交互式选择
        interactive_select
        
        # 检查是否有选择
        local has_selection=false
        for val in "${SKILL_SELECTED[@]}"; do
            if [[ "$val" == "1" ]]; then
                has_selection=true
                break
            fi
        done
        
        if [[ "$has_selection" == false ]]; then
            print_warning "未选择任何 Skills"
            exit 0
        fi
        
        # 选择目标目录
        clear
        print_header
        target_dir=$(select_target_directory)
        
        # 选择安装模式
        install_mode=$(select_install_mode)
        
        # 确认
        echo ""
        print_section "📋 确认安装"
        echo ""
        echo -e "目标目录: ${BOLD}$target_dir${NC}"
        echo -e "安装模式: ${BOLD}$install_mode${NC}"
        echo -e "选中的 Skills:"
        for i in "${!SKILL_NAMES[@]}"; do
            if [[ "${SKILL_SELECTED[$i]}" == "1" ]]; then
                echo -e "  - ${SKILL_NAMES[$i]}"
            fi
        done
        echo ""
        
        read -p "$(echo -e ${YELLOW}确认安装? [Y/n]: ${NC})" confirm
        confirm=${confirm:-Y}
        
        if [[ "$confirm" != "y" ]] && [[ "$confirm" != "Y" ]]; then
            print_info "已取消安装"
            exit 0
        fi
        
        # 执行安装
        perform_install "$target_dir" "$install_mode"
        
        # 显示使用提示
        show_usage_tips "$target_dir"
    fi
    
    echo -e "${GREEN}${BOLD}✨ 完成！${NC}"
    echo ""
}

# 运行主函数
main "$@"
