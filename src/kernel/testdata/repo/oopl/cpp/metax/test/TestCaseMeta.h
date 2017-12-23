#ifndef metax_test_TestCaseMeta_h
#define metax_test_TestCaseMeta_h 1

#include "metax/root/ObjectMetaRoot.h"

namespace metax {
namespace test {

// Auto-generated meta class for metax.test.TestCase.
class TestCaseMeta : public metax::root::ObjectMetaRoot {

  // field Debug : bool
  //   What to initialize TestCase.debug to.
  private: bool _Debug;
  public: virtual bool Debug() const { return this->_Debug; }
  public: virtual void DebugIs(bool value) { this->_Debug = value; }
  public: virtual bool& DebugRef() { return this->_Debug; }

  // field InstanceCount : int
  //   Counts the number of instances created so we can assign unique ids.
  //   Useful for debugging purposes.
  private: int32_t _InstanceCount;
  public: virtual int32_t InstanceCount() const { return this->_InstanceCount; }
  public: virtual void InstanceCountIs(int32_t value) { this->_InstanceCount = value; }
  public: virtual int32_t& InstanceCountRef() { return this->_InstanceCount; }

  // field WriteGoldens : bool
  //   If true, methods that invoke iseqstrgold() or iseqfilegold() will
  //   update goldens instead of compare goldens.
  private: bool _WriteGoldens;
  public: virtual bool WriteGoldens() const { return this->_WriteGoldens; }
  public: virtual void WriteGoldensIs(bool value) { this->_WriteGoldens = value; }
  public: virtual bool& WriteGoldensRef() { return this->_WriteGoldens; }

  // field CanonicalStdout : ostream
  //   The 'normal' stdout.
  private: std::ostream* _CanonicalStdout;
  public: virtual const std::ostream*const CanonicalStdout() const { return this->_CanonicalStdout; }
  public: virtual void CanonicalStdoutIs(std::ostream* value) { this->_CanonicalStdout = value; }
  public: virtual std::ostream*& CanonicalStdoutRef() { return this->_CanonicalStdout; }

  // field CanonicalStderr : ostream
  //   The 'normal' stderr.
  private: std::ostream* _CanonicalStderr;
  public: virtual const std::ostream*const CanonicalStderr() const { return this->_CanonicalStderr; }
  public: virtual void CanonicalStderrIs(std::ostream* value) { this->_CanonicalStderr = value; }
  public: virtual std::ostream*& CanonicalStderrRef() { return this->_CanonicalStderr; }

  // field Interactive : bool
  //   Set this to True to enable interactive unit tests.      
  private: bool _Interactive;
  public: virtual bool Interactive() const { return this->_Interactive; }
  public: virtual void InteractiveIs(bool value) { this->_Interactive = value; }
  public: virtual bool& InteractiveRef() { return this->_Interactive; }
  // Initialize class-level variables.  This includes variables for
  // controlling golden writing, interactivity, debugging, etc, based on
  // the value of envars.
  // 
  // TODO(wmh): This should be added to the 'meta lifecycle' above, when
  // support has been provided by Meta.
  public: TestCaseMeta(const std::string& name, std::vector<void**>& bases, std::map<std::string,void**>& symbols);
};
extern TestCaseMeta* MetaTestCase;

}  // test
}  // metax


#endif // metax_test_TestCaseMeta_h
