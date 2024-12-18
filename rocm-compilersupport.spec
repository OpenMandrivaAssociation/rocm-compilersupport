# The package follows LLVM's major version, but API version is still important:
%global comgr_maj_api_ver 2
%global comgr_full_api_ver %{comgr_maj_api_ver}.6.0
# LLVM information:
%global llvm_maj_ver 17
# If you bump LLVM, please reset bugfix_version to 0; I fork upstream sources,
# but I prepare the initial *.0 tag long before Fedora/EL picks up new LLVM.
# An LLVM update will require uploading new sources, contact mystro256 if FTBFS.
%global bugfix_version 0
%global upstreamname ROCm-CompilerSupport
 
Name:           rocm-compilersupport
Version:        %{llvm_maj_ver}.%{bugfix_version}
Release:        4
Summary:        Various AMD ROCm LLVM related services
 
Url:            https://github.com/RadeonOpenCompute/ROCm-CompilerSupport
License:        NCSA
# This is forked upstream sources because they don't target stable LLVM, but rather the
# bleeding edge LLVM branch. This fork is a snapshot with bugfixes backported:
Source0:        https://github.com/Mystro256/%{upstreamname}/archive/refs/tags/%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz
Patch0:		rocm-compilersupport-llvm-18.patch
 
BuildRequires:  cmake
BuildRequires:	ninja
BuildRequires:  clang-devel >= %{llvm_maj_ver}
BuildRequires:  clang
BuildRequires:  llvm-devel
BuildRequires:  llvm-static-devel
BuildRequires:  cmake(LLD)
BuildRequires:  rocm-device-libs
BuildRequires:  zlib-devel
BuildRequires:  libclc-amdgcn
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libxml-2.0)
 
%description
This package currently contains one library, the Code Object Manager (Comgr)
 
%package -n rocm-comgr
Summary:        AMD ROCm LLVM Code Object Manager
Provides:       comgr(major) = %{comgr_maj_api_ver}
Provides:       rocm-comgr = %{comgr_full_api_ver}-%{release}
 
%description -n rocm-comgr
The AMD Code Object Manager (Comgr) is a shared library which provides
operations for creating and inspecting code objects.
 
%package -n rocm-comgr-devel
Summary:        AMD ROCm LLVM Code Object Manager
Requires:       rocm-comgr%{?_isa} = %{version}-%{release}
 
%description -n rocm-comgr-devel
The AMD Code Object Manager (Comgr) development package.
 
The API is documented in the header file:
"%{_includedir}/amd_comgr.h"
 
%prep
%autosetup -p1 -n %{upstreamname}-%{version}
 
##Fix issue wit HIP, where compilation flags are incorrect, see issue:
#https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/issues/49
#Remove redundant includes:
sed -i '/Args.push_back(HIPIncludePath/,+1d' lib/comgr/src/comgr-compiler.cpp
sed -i '/Args.push_back(ROCMIncludePath/,+1d' lib/comgr/src/comgr-compiler.cpp
#Source hard codes the libdir too:
sed -i 's/lib\(\/clang\)/%{_lib}\1/' lib/comgr/src/comgr-compiler.cpp

cd lib/comgr
%cmake \
	-DBUILD_TESTING=ON \
	-G Ninja
 
%build
%ninja_build -C lib/comgr/build
 
%install
%ninja_install -C lib/comgr/build

%files -n rocm-comgr
%license LICENSE.txt lib/comgr/NOTICES.txt
%doc lib/comgr/README.md
%{_libdir}/libamd_comgr.so.%{comgr_full_api_ver}
%{_libdir}/libamd_comgr.so.%{comgr_maj_api_ver}
#Files already included:
%exclude %{_docdir}/amd_comgr*/LICENSE.txt
%exclude %{_docdir}/amd_comgr/NOTICES.txt
%exclude %{_docdir}/amd_comgr/README.md
 
%files -n rocm-comgr-devel
%{_includedir}/amd_comgr/amd_comgr.h
%{_libdir}/libamd_comgr.so
%{_libdir}/cmake/amd_comgr
#This header are deprecated and will be removed soon:
%{_includedir}/amd_comgr.h
