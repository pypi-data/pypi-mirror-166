#ifndef _CUDA_H_
#define _CUDA_H_


#define CUDA
// taken from pycuda._cluda
#define LOCAL_BARRIER __syncthreads()

#define WITHIN_KERNEL __device__
#define KERNEL extern "C" __global__
#define GLOBAL_MEM /* empty */
#define GLOBAL_MEM_ARG /* empty */
#define LOCAL_MEM __shared__
#define LOCAL_MEM_DYNAMIC extern __shared__
#define LOCAL_MEM_ARG /* empty */
#define CONSTANT_MEM __constant__
#define CONSTANT_MEM_ARG /* empty */
#define INLINE __forceinline__
#define SIZE_T int
#define VSIZE_T int

// used to align fields in structures
#define ALIGN(bytes) __align__(bytes)



WITHIN_KERNEL SIZE_T get_local_id(unsigned int dim)
{
    if(dim == 0) return threadIdx.x;
    if(dim == 1) return threadIdx.y;
    if(dim == 2) return threadIdx.z;
    return 0;
}

WITHIN_KERNEL SIZE_T get_group_id(unsigned int dim)
{
    if(dim == 0) return blockIdx.x;
    if(dim == 1) return blockIdx.y;
    if(dim == 2) return blockIdx.z;
    return 0;
}

WITHIN_KERNEL SIZE_T get_local_size(unsigned int dim)
{
    if(dim == 0) return blockDim.x;
    if(dim == 1) return blockDim.y;
    if(dim == 2) return blockDim.z;
    return 1;
}

WITHIN_KERNEL SIZE_T get_num_groups(unsigned int dim)
{
    if(dim == 0) return gridDim.x;
    if(dim == 1) return gridDim.y;
    if(dim == 2) return gridDim.z;
    return 1;
}

WITHIN_KERNEL SIZE_T get_global_size(unsigned int dim)
{
    return get_num_groups(dim) * get_local_size(dim);
}

WITHIN_KERNEL SIZE_T get_global_id(unsigned int dim)
{
    return get_local_id(dim) + get_group_id(dim) * get_local_size(dim);
}




#define COMPLEX_CTR(T) make_##T

WITHIN_KERNEL float2 operator+(float2 a, float2 b)
{
    return COMPLEX_CTR(float2)(a.x + b.x, a.y + b.y);
}
WITHIN_KERNEL float2 operator-(float2 a, float2 b)
{
    return COMPLEX_CTR(float2)(a.x - b.x, a.y - b.y);
}
WITHIN_KERNEL float2 operator+(float2 a) { return a; }
WITHIN_KERNEL float2 operator-(float2 a) { return COMPLEX_CTR(float2)(-a.x, -a.y); }
WITHIN_KERNEL double2 operator+(double2 a, double2 b)
{
    return COMPLEX_CTR(double2)(a.x + b.x, a.y + b.y);
}
WITHIN_KERNEL double2 operator-(double2 a, double2 b)
{
    return COMPLEX_CTR(double2)(a.x - b.x, a.y - b.y);
}
WITHIN_KERNEL double2 operator+(double2 a) { return a; }
WITHIN_KERNEL double2 operator-(double2 a) { return COMPLEX_CTR(double2)(-a.x, -a.y); }



#endif // _CUDA_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
